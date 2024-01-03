import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import AdmZip = require('adm-zip');
import { folder4Case, buffer2File, fire2csv } from './utils';

async function evacuationSpawn(folder: string, job: Job<unknown>) {
  const mcode = `addpath('${process.env.EVACUATION}'); Evacuation(); exit(0);`;
  console.log(mcode);
  const evacuationSpawn = spawn(
    process.env.MATLAB,
    [
      '-nodesktop',
      '-nosplash',
      '-noFigureWindows',
      '-softwareopengl',
      '-batch',
      mcode,
    ],
    { cwd: folder },
  );
  for await (const data of evacuationSpawn.stdout) {
    console.log(data.toString());
    const regex = /Current Generation.* (\d+) Remaining Generations (\d+)/;
    const match = regex.exec(data.toString());
    if (match) {
      const currentGeneration = parseInt(match[1]);
      const remainingGenerations = parseInt(match[2]);
      const totalGenerations = currentGeneration + remainingGenerations;

      const percentageCompleted =
        ((currentGeneration / totalGenerations) * 100 * 100) / 17.25;
      job.progress(percentageCompleted);
      console.log(`Completed: ${percentageCompleted}%`);
    }
    if (data.toString().includes('Completed')) {
      // await new Promise((resolve) => setTimeout(resolve, 5000));
      job.moveToCompleted('done', true);
    }
  }
  for await (const data of evacuationSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
  evacuationSpawn.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });
  evacuationSpawn.on('close', (code) => {
    console.log(`Child process closed with code: ${code.toString()}`);
  });

  evacuationSpawn.on('exit', (code) => {
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

@Processor('evacuation')
export class EvacuationConsumer {
  @Process({ name: 'evacuation-job', concurrency: 5 })
  async evacuationDo(job: Job<unknown>) {
    const folder = await folder4Case('evacuation', job);
    const buffer = Buffer.from(job.data['scase'][0]['buffer']['data']);
    if (job.data['isBIM']) {
      const fname = `${folder}/data.thcx`;
      await buffer2File(buffer, fname);
      await fire2csv(folder);
    } else {
      const fname = `${folder}/data.csv`;
      await buffer2File(buffer, fname);
    }
    await evacuationSpawn(folder, job);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    zip.writeZip(`${folder}/results.zip`);
    // console.log('EVACUATION DONE', zip.toBuffer());
    return zip.toBuffer();
  }
}
