import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import fs = require('fs');
import AdmZip = require('adm-zip');

import { OptimizeService } from './optimize.service';

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

async function prepareStrengthenCase(job: Job<unknown>): Promise<string> {
  const jobName = job.data['name'];
  const jobUUID = job.data['uuid'];
  const folder = `/tmp/imsafer/strengthen/${jobName}-${jobUUID}/`;
  const fname = `${folder}/Data.csv`;
  const buffer = Buffer.from(job.data['scase'][0]['buffer']['data']);
  await mkDir(folder);
  await buffer2File(buffer, fname);
  return folder;
}

async function strengthenSpawn(
  folder: string,
  job: Job<unknown>,
  service: OptimizeService
) {
  const mcode = `addpath('${process.env.STRENGTHEN}'); optimeccentricity('Data'); exit;`;

  const strengthenSpawn = spawn(
    process.env.MATLAB,
    [
      '-nodesktop',
      '-nosplash',
      '-noFigureWindows',
      '-softwareopengl',
      '-batch',
      mcode,
    ],
    { cwd: folder }
  );
  for await (const data of strengthenSpawn.stdout) {
    const regex =
      /.*Current emin:\W([0-9]*[.][0-9]*).*Remaining decades:\W(.*)/gm;
    const match = regex.exec(data.toString());
    if (match) {
      const percomplete = 2.5 * (40 - parseInt(match[2]));
      job.progress(percomplete);
      console.log(`Completed: ${percomplete}%`);
      const jobInfo = {
        progress: percomplete.toString(),
        processedOn: new Date(job.processedOn),
      };
      service.updateStrengthenJob(job.id.toString(), jobInfo);
    }
  }
  for await (const data of strengthenSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
  strengthenSpawn.on('exit', (code) => {
    const jobInfo = { finishedOn: new Date(job.finishedOn) };
    service.updateStrengthenJob(job.id.toString(), jobInfo);
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

@Processor('strengthen')
export class StrengthenConsumer {
  constructor(private service: OptimizeService) {}
  @Process('strengthen-job')
  async strengthenDo(job: Job<unknown>) {
    const folder = await prepareStrengthenCase(job);
    await strengthenSpawn(folder, job, this.service);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    return zip.toBuffer();
  }
}
