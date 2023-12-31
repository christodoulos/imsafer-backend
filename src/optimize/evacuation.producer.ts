import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class EvacuationProducer {
  constructor(@InjectQueue('evacuation') private readonly queue: Queue) {}

  async evacuationNew(scase: Express.Multer.File, name: string, uuid: string) {
    const isBIM = scase[0].originalname.split('.')[1] === 'thcx' ? true : false;
    const job = await this.queue.add('evacuation-job', {
      scase,
      name,
      uuid,
      isBIM,
    });

    return { jobID: job.id, name, uuid };
  }
}
