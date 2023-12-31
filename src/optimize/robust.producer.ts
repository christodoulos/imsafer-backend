import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class RobustProducer {
  constructor(@InjectQueue('robust') private readonly queue: Queue) {}

  async robustNew(scase: Express.Multer.File, name: string, uuid: string) {
    const job = await this.queue.add('robust-job', {
      scase,
      name,
      uuid,
    });

    return { jobID: job.id, name, uuid };
  }
}
