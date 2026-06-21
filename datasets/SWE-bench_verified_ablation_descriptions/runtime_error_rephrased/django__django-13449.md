On Django 3.0.7 with a SQLite database using the following model:  
from django.db import models  
class LagTest(models.Model):  
    modified = models.DateField()  
    data = models.FloatField()  
    amount = models.DecimalField(decimal_places=4, max_digits=7)  
  
and the following query:  
from django.db.models import F  
from django.db.models.functions import Lag  
from django.db.models import Window  
from test1.models import LagTest  
w = Window(expression=Lag('amount',7), partition_by=[F('modified')], order_by=F('modified').asc())  
q = LagTest.objects.all().annotate(w=w)  
  
generates the following error:  
When Django tries to run this query, SQLite reports an OperationalError citing a syntax error near “OVER.” The SQL it’s attempting is effectively:  
SELECT …, CAST(LAG("test1_lagtest"."amount", 7) AS NUMERIC) OVER (PARTITION BY "test1_lagtest"."modified" ORDER BY "test1_lagtest"."modified" ASC) AS "w" …  
SQLite doesn’t accept the OVER clause in that context because the CAST only covers the LAG() call, causing the parser to choke on the misplaced OVER.  
  
I believe this fails as the CAST() statement ends after LAG whereas it should be around the whole statement up until "w"  
This only applies where the lagged field is a DecimalField e.g.  
w = Window(expression=Lag('data',7), partition_by=[F('modified')], order_by=F('modified').asc())  
works correctly.  
I can override it by adding output_field=FloatField() to the Lag function e.g.  
w = Window(expression=Lag('amount',7,output_field=FloatField()), partition_by=[F('modified')], order_by=F('modified').asc())