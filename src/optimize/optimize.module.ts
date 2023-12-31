import { Module } from '@nestjs/common';
import { OptimizeController } from './optimize.controller';
import { BullModule } from '@nestjs/bull';

import { BlastProducer } from './blast.producer';
import { BlastConsumer } from './blast.consumer';
import { FireProducer } from './fire.producer';
import { FireConsumer } from './fire.consumer';
import { RobustProducer } from './robust.producer';
import { RobustConsumer } from './robust.consumer';

@Module({
  imports: [
    BullModule.registerQueue(
      { name: 'robust' },
      { name: 'blast' },
      { name: 'fire' },
    ),
  ],
  controllers: [OptimizeController],
  providers: [
    BlastProducer,
    BlastConsumer,
    FireProducer,
    FireConsumer,
    RobustProducer,
    RobustConsumer,
  ],
})
export class OptimizeModule {}
