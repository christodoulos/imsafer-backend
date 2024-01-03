import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class AssessmentProducer {
  constructor(@InjectQueue('assessment') private readonly queue: Queue) {}

  async assessmentNew(scase: Express.Multer.File, name: string, uuid: string) {
    const isBIM = scase[0].originalname.split('.')[1] === 'thcx' ? true : false;
    const job = await this.queue.add('assessment-job', {
      scase,
      name,
      uuid,
      isBIM,
    });

    return { jobID: job.id, name, uuid };
  }
}
