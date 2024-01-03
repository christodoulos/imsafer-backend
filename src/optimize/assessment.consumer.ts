import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import AdmZip = require('adm-zip');
import { folder4Case, buffer2File, assess2csv } from './utils';

async function assessmentSpawn(folder: string, job: Job<unknown>) {
  const mcode = `addpath('${process.env.ASSESSMENT}'); optimeccentricity('Data'); exit(0);`;
  console.log(mcode);
  const assessmentSpawn = spawn(
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
  for await (const data of assessmentSpawn.stdout) {
    const regex =
      /.*Current emin:\W([0-9]*[.][0-9]*).*Remaining decades:\W(.*)/gm;
    const match = regex.exec(data.toString());
    if (match) {
      const percomplete = 2.5 * (40 - parseInt(match[2]));
      job.progress(percomplete);
      console.log(`Completed: ${percomplete}%`);
      if (percomplete == 100) {
        job.moveToCompleted('done', true);
      }
    }
  }
  for await (const data of assessmentSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
  assessmentSpawn.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });
  assessmentSpawn.on('close', (code) => {
    console.log(`Child process closed with code: ${code.toString()}`);
  });

  assessmentSpawn.on('exit', (code) => {
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

@Processor('assessment')
export class AssessmentConsumer {
  @Process({ name: 'assessment-job', concurrency: 5 })
  async assessmentDo(job: Job<unknown>) {
    const folder = await folder4Case('assessment', job);
    const buffer = Buffer.from(job.data['scase'][0]['buffer']['data']);
    if (job.data['isBIM']) {
      const fname = `${folder}/Data.thcx`;
      await buffer2File(buffer, fname);
      await assess2csv(folder);
    } else {
      const fname = `${folder}/Data.csv`;
      await buffer2File(buffer, fname);
    }
    await assessmentSpawn(folder, job);

    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    zip.writeZip(`${folder}/results.zip`);
    console.log('ASSESSMENT DONE', zip.toBuffer());

    return zip.toBuffer();
  }
}