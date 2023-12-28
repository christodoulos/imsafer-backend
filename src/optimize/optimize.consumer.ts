import { Process, Processor } from '@nestjs/bull';
import { Job } from 'bull';

@Processor('optimize')
export class OptimizeConsumer {
  @Process('optimize-job')
  readOptimizeJob(job: Job<unknown>) {
    console.log(job.data);
    return 1222;
  }
}
