make temporal subtraction work without ExpressionWrapper  
Description  

class Experiment(models.Model):  
	start = models.DateTimeField()  
	end = models.DateTimeField()  
Experiment.objects.annotate(  
	delta=F('end') - F('start') + Value(datetime.timedelta(), output_field=DurationField())  
)  
When this runs, Django raises a FieldError because the annotation is combining a DateTimeField with a DurationField without an explicit output_field.