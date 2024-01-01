import { Job } from 'bull';
import fs = require('fs');

const fsPromises = fs.promises;

export type JobType = 'evacuation' | 'robust' | 'blast' | 'fire';

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
    fsPromises.writeFile(fname, buffer.toString());
    console.log('Successful buffer dump to file');
  } catch (err) {
    console.error('Error while writing buffer to file!', err);
  }
}
