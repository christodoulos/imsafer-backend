import { Job } from 'bull';
import fs = require('fs');
import { spawn } from 'child_process';

const fsPromises = fs.promises;

export type JobType = 'evacuation' | 'robust' | 'blast' | 'fire' | 'assessment';

async function mkDir(name: string) {
  try {
    return await fsPromises.mkdir(name, { recursive: true });
  } catch (err) {
    console.error('Error while making directory!', err);
  }
}

export async function folder4Case(
  jobType: JobType,
  job: Job<unknown>,
): Promise<string> {
  const jobName = job.data['name'];
  const jobUUID = job.data['uuid'];
  const folder = `/tmp/imsafer/${jobType}/${jobName}-${jobUUID}/`;
  await mkDir(folder);
  return folder;
}

export async function string2File(s: string, fname: string) {
  try {
    fsPromises.writeFile(fname, s);
    console.log('Successful string dump to file');
  } catch (err) {
    console.error('Error while writing string to file!', err);
  }
}

export async function buffer2File(buffer: Buffer, fname: string) {
  try {
    fsPromises.writeFile(fname, buffer);
    console.log('Successful buffer dump to file');
  } catch (err) {
    console.error('Error while writing buffer to file!', err);
  }
}

export async function fire2csv(folder: string) {
  const fname = `${folder}/data.thcx`;
  const fire2csvSpawn = spawn(process.env.FIRE2CSV, [fname], { cwd: folder });
  fire2csvSpawn.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });
  fire2csvSpawn.on('exit', (code) => {
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}

export async function assess2csv(folder: string) {
  const fname = `${folder}/Data.thcx`;
  const fire2csvSpawn = spawn(process.env.ASSESS2CSV, [fname], { cwd: folder });
  fire2csvSpawn.on('error', (error) => {
    console.error(`An error occurred: ${error.message}`);
  });
  fire2csvSpawn.on('exit', (code) => {
    console.log(`Child process exited with code: ${code.toString()}`);
  });
}
