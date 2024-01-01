import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class EvacuationProducer {
  constructor(@InjectQueue('evacuation') private readonly queue: Queue) {}

  async robustNew(scase: Express.Multer.File, name: string, uuid: string) {
    const job = await this.queue.add('evacuation-job', {
      scase,
      name,
      uuid,
    });

    return { jobID: job.id, name, uuid };
  }
}
