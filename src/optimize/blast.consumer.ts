import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';
import { spawn } from 'child_process';
import AdmZip = require('adm-zip');
import { folder4Case } from './utils';

async function blastSpawn(folder: string, job: Job<unknown>) {
  const {
    chargeWeight,
    distance,
    structureWidth,
    structureLength,
    structureHeight,
  } = job.data['blastData'];

  console.log('BLAST DATA', job.data['blastData'], process.env.BLAST);
  const blastSpawn = spawn(
    process.env.BLAST,
    [chargeWeight, distance, structureWidth, structureLength, structureHeight],
    { cwd: folder },
  );
  console.log(blastSpawn.pid);
  for await (const data of blastSpawn.stderr) {
    job.failedReason = data.toString();
    job.moveToFailed({ message: job.failedReason }, true);
  }
}

@Processor('blast')
export class BlastConsumer {
  @Process({ name: 'blast-job', concurrency: 5 })
  async blastDo(job: Job<unknown>) {
    const folder = await folder4Case('blast', job);
    console.log(folder);
    await blastSpawn(folder, job);
    const zip = new AdmZip();
    zip.addLocalFolder(folder);
    return zip.toBuffer();
  }
}
