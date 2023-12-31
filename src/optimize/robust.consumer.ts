import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import fs = require('fs');
import AdmZip = require('adm-zip');

const fsPromises = fs.promises;

async function mkDir(name: string) {
  try {
    return await fsPromises.mkdir(name, { recursive: true });
  } catch (err) {
    console.error('Error while making directory!', err);
  }
}

async function buffer2File(buffer: Buffer, fname: string) {
  try {
    fsPromises.writeFile(fname, buffer.toString());
    console.log('Successful buffer dump to file');
  } catch (err) {
    console.error('Error while writing buffer to file!', err);
  }
}

async function prepareRobustCase(job: Job<unknown>): Promise<string> {
  const jobName = job.data['name'];
  const jobUUID = job.data['uuid'];
  const folder = `/tmp/imsafer/robust/${jobName}-${jobUUID}/`;
  const fname = `${folder}/Data.csv`;
  const buffer = Buffer.from(job.data['scase'][0]['buffer']['data']);
  await mkDir(folder);
  await buffer2File(buffer, fname);
  return folder;
}

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
  @Process('robust-job')
  async robustDo(job: Job<unknown>) {
    const folder = await prepareRobustCase(job);
    await robustSpawn(folder, job);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    return zip.toBuffer();
  }
}
