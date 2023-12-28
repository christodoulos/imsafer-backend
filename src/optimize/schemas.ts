import { Prop, Schema, SchemaFactory } from '@nestjs/mongoose';
import { Document } from 'mongoose';
// import validator from 'validator';

export type StrengthenDocument = Strengthen & Document;

@Schema()
export class Strengthen {
  @Prop({ required: true })
  name!: string;

  @Prop({ default: 0 })
  jobID!: string;

  @Prop({ default: '' })
  jobUUID!: string;

  @Prop()
  timestamp!: Date;

  @Prop()
  finishedOn!: Date;

  @Prop()
  processedOn!: Date;

  @Prop()
  progress!: string;
}

export const StrengthenSchema = SchemaFactory.createForClass(Strengthen);
