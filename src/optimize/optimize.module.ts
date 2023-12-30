import { Module } from '@nestjs/common';
import { OptimizeController } from './optimize.controller';
import { BullModule } from '@nestjs/bull';

import { BlastProducer } from './blast.producer';
import { BlastConsumer } from './blast.consumer';
import { FireProducer } from './fire.producer';
import { FireConsumer } from './fire.consumer';

@Module({
  imports: [
    BullModule.registerQueue(
      { name: 'robust' },
      { name: 'blast' },
      { name: 'fire' },
    ),
  ],
  controllers: [OptimizeController],
  providers: [BlastProducer, BlastConsumer, FireProducer, FireConsumer],
})
export class OptimizeModule {}
