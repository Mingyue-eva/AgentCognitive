make temporal subtraction work without ExpressionWrapper  
Description

I have an Experiment model with two DateTimeFields, start and end. I try to annotate the queryset so that each record gets a delta equal to end minus start, plus a zero-length interval to force a DurationField result. I expect to get the time difference between end and start for each object.

This gives:
django.core.exceptions.FieldError: Expression contains mixed types: DateTimeField, DurationField. You must set output_field.