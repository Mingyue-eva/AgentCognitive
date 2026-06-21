make temporal subtraction work without ExpressionWrapper  
Description  

To reproduce the issue, define an Experiment model with two DateTime fields named start and end. Then run a query that annotates each Experiment record by subtracting the start time from the end time and adding a zero-length duration. You would expect the query to return each record with an extra field showing the time interval between end and start.  

When this annotation is executed, it fails at runtime with a field error. The failure happens because the database expression is combining a datetime value and a duration value without an explicit output type, and the system reports that mixed types require an output_field.