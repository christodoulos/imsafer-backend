import { InjectQueue } from '@nestjs/bull';
import {
  Body,
  Controller,
  Get,
  Header,
  Param,
  Post,
  Res,
  StreamableFile,
  UseInterceptors,
} from '@nestjs/common';
import { AnyFilesInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';
import { Queue } from 'bull';

import { BlastProducer } from './blast.producer';
import { FireProducer } from './fire.producer';
import { nanoid } from 'nanoid';
import { createReadStream } from 'fs';

@Controller('optimize')
export class OptimizeController {
  constructor(
    @InjectQueue('blast') private readonly blastQueue: Queue,
    @InjectQueue('fire') private readonly fireQueue: Queue,
    private readonly blastProducer: BlastProducer,
    private readonly fireProducer: FireProducer,
  ) {}

  @Post('blast')
  @UseInterceptors(AnyFilesInterceptor())
  async processBlastCase(@Body() body) {
    console.log('BLAST CONTROLLER', body);
    const uuid = nanoid();
    return this.blastProducer.blastNew(body.name, JSON.parse(body.data), uuid);
  }

  @Get('blastResults/:id')
  async blastResults(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.blastQueue.getJob(id);
    const name = job.data['name'];
    res.set({
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${name}.zip"`,
    });
    const result = Buffer.from(job.returnvalue);
    return new StreamableFile(result);
  }

  @Get('blast/:id')
  async getBlastResults(@Res() res: Response, @Param('id') id: string) {
    const job = await this.blastQueue.getJob(id);
    const jobIsCompleted = await job.isCompleted();
    const jobHasFailed = await job.isFailed();
    let failedReason = '';
    if (jobHasFailed) failedReason = job.failedReason;
    res.send({
      completed: jobIsCompleted,
      failed: jobHasFailed,
      failedReason: failedReason,
    });
  }

  @Get('blast/:id/picture')
  @Header('Content-Type', 'image/png')
  @Header('Content-Disposition', 'attachment; filename=plot.png')
  async getBlastResultPicture(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.blastQueue.getJob(id);
    const { name, uuid } = job.data;
    const plot = `/tmp/imsafer/blast/${name}-${uuid}/plot.png`;
    const data = createReadStream(plot);
    return new StreamableFile(data);
  }

  @Post('fire')
  @UseInterceptors(AnyFilesInterceptor())
  async processFireCase(@Body() body: { name: string; atc: string }) {
    console.log('FIRE CONTROLLER', body);
    const uuid = nanoid();
    return this.fireProducer.fireNew(body.name, body.atc, uuid);
  }

  @Get('fire')
  async getAllFireJobs() {
    return this.fireQueue.getJobs([
      'active',
      'completed',
      'delayed',
      'failed',
      'paused',
      'waiting',
    ]);
  }

  @Get('fire/:id')
  async getFireResults(@Res() res: Response, @Param('id') id: string) {
    const job = await this.fireQueue.getJob(id);
    const jobIsCompleted = await job.isCompleted();
    const jobHasFailed = await job.isFailed();
    const progress = job.progress();
    let failedReason = '';
    if (jobHasFailed) failedReason = job.failedReason;
    res.send({
      completed: jobIsCompleted,
      failed: jobHasFailed,
      failedReason: failedReason,
      progress: progress,
    });
  }

  @Get('fireResults/:id')
  async fireResults(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.fireQueue.getJob(id);
    const name = job.data['name'];
    res.set({
      'Content-Type': 'text/plain',
      'Content-Disposition': `attachment; filename="${name}.txt`,
    });
    const result = Buffer.from(job.returnvalue);
    return new StreamableFile(result);
  }
}
