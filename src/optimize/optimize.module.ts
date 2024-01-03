import { Module } from '@nestjs/common';
import { OptimizeController } from './optimize.controller';
import { BullModule } from '@nestjs/bull';

import { BlastProducer } from './blast.producer';
import { BlastConsumer } from './blast.consumer';
import { FireProducer } from './fire.producer';
import { FireConsumer } from './fire.consumer';
import { RobustProducer } from './robust.producer';
import { RobustConsumer } from './robust.consumer';
import { EvacuationProducer } from './evacuation.producer';
import { EvacuationConsumer } from './evacuation.consumer';
import { AssessmentProducer } from './assessment.producer';
import { AssessmentConsumer } from './assessment.consumer';

@Module({
  imports: [
    BullModule.registerQueue(
      { name: 'robust' },
      { name: 'blast' },
      { name: 'fire' },
      { name: 'evacuation' },
      { name: 'assessment' },
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
    EvacuationProducer,
    EvacuationConsumer,
    AssessmentProducer,
    AssessmentConsumer,
  ],
})
export class OptimizeModule {}
