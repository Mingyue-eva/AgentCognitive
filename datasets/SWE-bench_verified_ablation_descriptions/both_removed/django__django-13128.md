make temporal subtraction work without ExpressionWrapper

Description

Attempting to annotate the difference between two DateTimeField attributes and adding a timedelta value triggers a FieldError about mixed types, even when providing an output_field. It would be ideal to support temporal subtraction natively without requiring ExpressionWrapper.