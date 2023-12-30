import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class RobustProducer {
  constructor(@InjectQueue('robust') private readonly queue: Queue) {}

  async robustNew(name: string, data: any, uuid: string) {
    const job = await this.queue.add('robust-job', {
      name,
      robustData: data,
      uuid,
    });

    return { jobID: job.id, name, uuid };
  }
}
