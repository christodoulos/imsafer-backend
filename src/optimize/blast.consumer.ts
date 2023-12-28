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

async function prepareBlastCase(job: Job<unknown>): Promise<string> {
  const jobName = job.data['name'];
  const jobUUID = job.data['uuid'];
  const folder = `/tmp/imsafer/blast/${jobName}-${jobUUID}/`;
  await mkDir(folder);
  return folder;
}

async function blastSpawn(folder: string, job: Job<unknown>) {
  const {
    chargeWeight,
    distance,
    structureWidth,
    structureLength,
    structureHeight,
  } = job.data['blastData'];

  const blastSpawn = spawn(
    process.env.BLAST,
    [chargeWeight, distance, structureWidth, structureLength, structureHeight],
    { cwd: folder },
  );
  for await (const data of blastSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
}

@Processor('blast')
export class BlastConsumer {
  @Process('blast-job')
  async blastDo(job: Job<unknown>) {
    const folder = await prepareBlastCase(job);
    await blastSpawn(folder, job);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    return zip.toBuffer();
  }
}
