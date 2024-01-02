import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import AdmZip = require('adm-zip');
import { folder4Case, buffer2File } from './utils';

async function robustSpawn(folder: string, job: Job<unknown>) {
  const mcode = `addpath('${process.env.ROBUST}'); optimeccentricity('Data'); exit;`;

  const robustSpawn = spawn(
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
  for await (const data of robustSpawn.stdout) {
    const regex =
      /.*Current emin:\W([0-9]*[.][0-9]*).*Remaining decades:\W(.*)/gm;
    const match = regex.exec(data.toString());
    if (match) {
      const percomplete = 2.5 * (40 - parseInt(match[2]));
      job.progress(percomplete);
      console.log(`Completed: ${percomplete}%`);
      if (percomplete === 100) {
        job.moveToCompleted('done', true);
      }
    }
  }
  for await (const data of robustSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
  robustSpawn.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });
  robustSpawn.on('close', (code) => {
    console.log(`Child process closed with code: ${code.toString()}`);
  });

  robustSpawn.on('exit', (code) => {
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

@Processor('robust')
export class RobustConsumer {
  @Process({ name: 'robust-job', concurrency: 5 })
  async robustDo(job: Job<unknown>) {
    const folder = await folder4Case('robust', job);
    const fname = `${folder}/Data.csv`;
    const buffer = Buffer.from(job.data['scase'][0]['buffer']['data']);
    await buffer2File(buffer, fname);
    await robustSpawn(folder, job);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    return zip.toBuffer();
  }
}
