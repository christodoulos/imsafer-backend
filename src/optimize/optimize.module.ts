import { Module } from '@nestjs/common';
import { OptimizeController } from './optimize.controller';
import { BullModule } from '@nestjs/bull';

import { OptimizeProducer } from './optimize.producer';
import { StrengthenProducer } from './strengthen.producer';
import { MongooseModule } from '@nestjs/mongoose';
import { Strengthen, StrengthenSchema } from './schemas';
import { OptimizeService } from './optimize.service';
import { StrengthenConsumer } from './strengthen.consumer';
import { BlastProducer } from './blast.producer';
import { BlastConsumer } from './blast.consumer';

@Module({
  imports: [
    MongooseModule.forFeature([
      { name: Strengthen.name, schema: StrengthenSchema },
    ]),
    BullModule.registerQueue(
      { name: 'optimize' },
      { name: 'strengthen' },
      { name: 'blast' },
    ),
  ],
  controllers: [OptimizeController],
  providers: [
    OptimizeProducer,
    StrengthenProducer,
    StrengthenConsumer,
    BlastProducer,
    BlastConsumer,
    OptimizeService,
  ],
})
export class OptimizeModule {}
