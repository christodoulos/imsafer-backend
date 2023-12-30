import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';
import { BlastJob } from './interfaces';

@Injectable()
export class BlastProducer {
  constructor(@InjectQueue('blast') private readonly queue: Queue) {}

  async blastNew(name: string, data: BlastJob, uuid: string) {
    const job = await this.queue.add('blast-job', {
      name,
      blastData: data,
      uuid,
    });

    return { jobID: job.id, name, uuid };
  }
}
