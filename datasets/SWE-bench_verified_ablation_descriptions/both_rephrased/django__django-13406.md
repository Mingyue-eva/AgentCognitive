Queryset with values()/values_list() crashes when recreated from a pickled query  
Description  
I am pickling query objects (queryset.query) for later re-evaluation as per https://docs.djangoproject.com/en/2.2/ref/models/querysets/#pickling-querysets. However, when I tried to rerun a query that combines values and annotate for a GROUP BY functionality, the result is broken.  
Normally, the result of the query is and should be a list of dicts, but in this case instances of the model are returned, but their internal state is broken and it is impossible to even access their .id because of a AttributeError: 'NoneType' object has no attribute 'attname' error.  
I created a minimum reproducible example.  

models.py  
from django.db import models  
class Toy(models.Model):  
    name = models.CharField(max_length=16)  
    material = models.CharField(max_length=16)  
    price = models.PositiveIntegerField()  

Reproduction steps and expected result  
First, populate the database with three Toy records having different names, materials, and prices. Next, run a grouping query that selects the material field and annotates the total price for each material; this should yield a list of dictionaries, each containing a material name and its aggregated price. Then take an unmodified Toy queryset, serialize and deserialize its underlying query object, and assign this restored query to a new queryset. When you inspect the first queryset’s first item, you see a dictionary as expected. After replacing the query on the second queryset, inspecting its first item unexpectedly shows a Toy model instance rather than a dict. The expected behavior is for both querysets to return identical dictionaries.  

Runtime error observation  
When attempting to convert the queryset returned from the deserialized query into its string representation or access its primary key, Django tries to build model instances from the grouped data but fails because an internal model field reference is missing. This leads to an AttributeError indicating that a NoneType object does not have the expected attribute.