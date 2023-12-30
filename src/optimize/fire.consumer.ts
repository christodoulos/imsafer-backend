import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import fs = require('fs');

const fsPromises = fs.promises;

async function mkDir(name: string) {
  try {
    return await fsPromises.mkdir(name, { recursive: true });
  } catch (err) {
    console.error('Error while making directory!', err);
  }
}

async function string2File(s: string, fname: string) {
  try {
    fsPromises.writeFile(fname, s);
    console.log('Successful atc dump to file');
  } catch (err) {
    console.error('Error while writing string to file!', err);
  }
}

async function prepareFireCase(job: Job<unknown>): Promise<string> {
  const jobName = job.data['name'];
  const jobUUID = job.data['uuid'];
  const folder = `/tmp/imsafer/fire/${jobName}-${jobUUID}/`;
  const fname = `${folder}/ex.atc`;
  await mkDir(folder);
  await string2File(job.data['fireData'], fname);
  return folder;
}

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
  @Process('fire-job')
  async fireDo(job: Job<unknown>) {
    const folder = await prepareFireCase(job);
    await fireSpawn(folder, job);
    const result = await fsPromises.readFile(`${folder}/ex.res`);
    return result;
  }
}
