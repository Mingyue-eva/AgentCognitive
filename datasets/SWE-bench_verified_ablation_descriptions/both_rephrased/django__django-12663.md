Using SimpleLazyObject with a nested subquery annotation fails.  
Description  
     
    (last modified by Jordan Ephron)  
     
Prior to 35431298226165986ad07e91f9d3aca721ff38ec it was possible to use a SimpleLazyObject in a queryset as demonstrated below. This new behavior appears to be a regression.  
Models  
from django.contrib.auth.models import User  
from django.db import models  
class A(models.Model):  
    pass  
class B(models.Model):  
    a = models.ForeignKey(A, on_delete=models.CASCADE)  
class C(models.Model):  
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  

TestCase  
To reproduce the issue, you first build a subquery on model B that finds the related owner from model C and annotate that owner ID onto model A. Next you create a Django user through a SimpleLazyObject so that the actual user is created only when accessed. Finally you apply a filter on the A queryset, comparing the annotated owner_user field to the lazy user object. Under the new code this filter attempt triggers an error.  

Results  
When the filter is applied, Django tries to prepare the lookup by converting the provided value to the field’s native type, which in this case is an integer. Because the value is still wrapped in a SimpleLazyObject rather than a raw integer or user instance, the conversion fails and a type error is raised, indicating that int() cannot accept a SimpleLazyObject.