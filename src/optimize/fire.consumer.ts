import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import { folder4Case, string2File } from './utils';
import fs = require('fs');

const fsPromises = fs.promises;

async function fireSpawn(folder: string, job: Job<unknown>) {
  const regex = /Iteration (.*) (.*) condition (.*) (.*)/gm;
  const fireSpawn = spawn(process.env.FIRE, ['ex'], { cwd: folder });
  for await (const data of fireSpawn.stdout) {
    const match = regex.exec(data.toString());
    if (match) {
      console.log(match[1], match[2], match[3], match[4]);
      const isActive = await job.isActive();
      if (isActive) {
        const percomplete = (parseInt(match[1]) / parseInt(match[2])) * 100;
        job.progress(percomplete);
      }
    }
  }
  for await (const data of fireSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
  fireSpawn.on('exit', (code) => {
    if (code === 0) job.progress(100);
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

@Processor('fire')
export class FireConsumer {
  @Process({ name: 'fire-job', concurrency: 5 })
  async fireDo(job: Job<unknown>) {
    const folder = await folder4Case('fire', job);
    const fname = `${folder}/ex.atc`;
    await string2File(job.data['fireData'], fname);
    await fireSpawn(folder, job);
    const result = await fsPromises.readFile(`${folder}/ex.res`);
    return result;
  }
}
