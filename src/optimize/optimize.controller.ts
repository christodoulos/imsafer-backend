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
  UploadedFiles,
  UseInterceptors,
} from '@nestjs/common';
import { AnyFilesInterceptor } from '@nestjs/platform-express';
import { Response } from 'express';
import { Queue } from 'bull';
import { nanoid } from 'nanoid';
import { createReadStream } from 'fs';

import { BlastProducer } from './blast.producer';
import { FireProducer } from './fire.producer';
import { RobustProducer } from './robust.producer';
import { EvacuationProducer } from './evacuation.producer';
import { AssessmentProducer } from './assessment.producer';

@Controller('optimize')
export class OptimizeController {
  constructor(
    @InjectQueue('blast') private readonly blastQueue: Queue,
    @InjectQueue('fire') private readonly fireQueue: Queue,
    @InjectQueue('robust') private readonly robustQueue: Queue,
    @InjectQueue('evacuation') private readonly evacuationQueue: Queue,
    @InjectQueue('assessment') private readonly assessmentQueue: Queue,
    private readonly blastProducer: BlastProducer,
    private readonly fireProducer: FireProducer,
    private readonly robustProducer: RobustProducer,
    private readonly evacuationProducer: EvacuationProducer,
    private readonly assessmentProducer: AssessmentProducer,
  ) {}

  // BLAST /////////////////////////////////////////////////

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

  // FIRE /////////////////////////////////////////////////

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

  // ROBUST /////////////////////////////////////////////////

  @Post('robust')
  @UseInterceptors(AnyFilesInterceptor())
  async processRobustCase(
    @UploadedFiles() file: Express.Multer.File,
    @Body() body: { name: string },
  ) {
    console.log('ROBUST POST', body);
    const uuid = nanoid();
    return this.robustProducer.robustNew(file, body.name, uuid);
  }

  @Get('robust/:id')
  async getRobustResults(@Res() res: Response, @Param('id') id: string) {
    const job = await this.robustQueue.getJob(id);
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

  @Get('robust/:id/picture')
  @Header('Content-Type', 'image/jpg')
  @Header('Content-Disposition', 'attachment; filename=plot.jpg')
  async getRobustResultPicture(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.robustQueue.getJob(id);
    console.log(job);
    const { name, uuid } = job.data;
    const plot = `/tmp/imsafer/robust/${name}-${uuid}/Data_r.jpg`;
    const data = createReadStream(plot);
    return new StreamableFile(data);
  }

  @Get('robustResults/:id')
  async robustResults(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.robustQueue.getJob(id);
    const name = job.data['name'];
    res.set({
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${name}.zip"`,
    });
    const result = Buffer.from(job.returnvalue);
    return new StreamableFile(result);
  }

  // EVACUATION /////////////////////////////////////////////////

  @Post('evacuation')
  @UseInterceptors(AnyFilesInterceptor())
  async processEvacuationCase(
    @UploadedFiles() file: Express.Multer.File,
    @Body() body: { name: string },
  ) {
    console.log('EVACUATION POST', body);
    const uuid = nanoid();
    return this.evacuationProducer.evacuationNew(file, body.name, uuid);
  }

  @Get('evacuation/:id')
  async getEvacuationResults(@Res() res: Response, @Param('id') id: string) {
    console.log('EVACUATION GET', id);
    const job = await this.evacuationQueue.getJob(id);
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

  @Get('evacuationResults/:id')
  async evacuationResults(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.evacuationQueue.getJob(id);
    const name = job.data['name'];
    res.set({
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${name}.zip"`,
    });
    const result = Buffer.from(job.returnvalue);
    return new StreamableFile(result);
  }

  // ASSESSMENT /////////////////////////////////////////////////

  @Post('assessment')
  @UseInterceptors(AnyFilesInterceptor())
  async processAssessmentCase(
    @UploadedFiles() file: Express.Multer.File,
    @Body() body: { name: string },
  ) {
    console.log('ASSESSMENT POST', body);
    const uuid = nanoid();
    return this.assessmentProducer.assessmentNew(file, body.name, uuid);
  }

  @Get('assessment/:id')
  async getAssessmentResults(@Res() res: Response, @Param('id') id: string) {
    console.log('ASSESSMENT GET', id);
    const job = await this.assessmentQueue.getJob(id);
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

  @Get('assessment/:id/picture')
  @Header('Content-Type', 'image/jpg')
  @Header('Content-Disposition', 'attachment; filename=plot.jpg')
  async getAssessmentResultPicture(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.assessmentQueue.getJob(id);
    console.log(job);
    const { name, uuid } = job.data;
    const plot = `/tmp/imsafer/assessment/${name}-${uuid}/Data_r.jpg`;
    const data = createReadStream(plot);
    return new StreamableFile(data);
  }

  @Get('assessmentResults/:id')
  async assessmentResults(
    @Res({ passthrough: true }) res: Response,
    @Param('id') id: string,
  ): Promise<StreamableFile> {
    const job = await this.assessmentQueue.getJob(id);
    const name = job.data['name'];
    res.set({
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${name}.zip"`,
    });
    const result = Buffer.from(job.returnvalue);
    return new StreamableFile(result);
  }
}
