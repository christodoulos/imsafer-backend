import { Injectable } from '@nestjs/common';
import { Model } from 'mongoose';
import { Strengthen, StrengthenDocument } from './schemas';
import { InjectModel } from '@nestjs/mongoose';

@Injectable()
export class OptimizeService {
  constructor(
    @InjectModel(Strengthen.name) private model: Model<StrengthenDocument>,
  ) {}

  async findAllStrengthen(): Promise<Strengthen[]> {
    return this.model.find().exec();
  }

  async saveStrengthenJob(
    name: string,
    jobID: string,
    timestamp: Date,
    jobUUID: string,
  ) {
    const createdJob = new this.model({ name, jobID, timestamp, jobUUID });
    return await createdJob.save();
  }

  async updateStrengthenJob(
    jobID: string,
    jobInfo: {
      timestamp?: Date;
      finishedOn?: Date;
      processedOn?: Date;
      progress?: string;
    },
  ) {
    const foundJob = await this.model.findOne({ jobID });
    if (foundJob) {
      if (jobInfo.timestamp) foundJob.timestamp = jobInfo.timestamp;
      if (jobInfo.finishedOn) foundJob.finishedOn = jobInfo.finishedOn;
      if (jobInfo.processedOn) foundJob.processedOn = jobInfo.processedOn;
      if (jobInfo.progress) foundJob.progress = jobInfo.progress;
      await foundJob.save();
    }
  }

  async findNameByJobID(jobID: string) {
    const foundJob = await this.model.findOne({ jobID });
    return foundJob.name;
  }
}
