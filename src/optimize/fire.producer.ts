import { InjectQueue } from '@nestjs/bull';
import { Injectable } from '@nestjs/common';
import { Queue } from 'bull';

export interface FireJob {
  atc: string;
}

@Injectable()
export class FireProducer {
  constructor(@InjectQueue('fire') private readonly queue: Queue) {}

  async fireNew(name: string, atc: string, uuid: string) {
    const job = await this.queue.add(
      'fire-job',
      { name, fireData: atc, uuid },
      { attempts: 5, backoff: 10000 },
    );
    return { jobID: job.id, name, uuid };
  }
}
