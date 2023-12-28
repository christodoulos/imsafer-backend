import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

@Injectable()
export class OptimizeProducer {
  constructor(@InjectQueue('optimize') private readonly optimizeQueue: Queue) {}

  async strengthenCase(files: Express.Multer.File[]) {
    const job = await this.optimizeQueue.add('optimize-job', {
      files,
    });

    return {
      jobId: job.id,
    };
  }
}
