Lag() with DecimalField crashes on SQLite.  
Description  

To reproduce this issue, use Django 3.0.7 with a SQLite database and define a model that has a DateField called modified, a FloatField called data, and a DecimalField called amount. Then build a queryset that annotates each row with a window function computing the value of amount seven rows earlier, partitioning by modified and ordering by modified ascending. You would expect the query to complete successfully and return each record along with its lagged amount.  

When you execute this queryset (for example, by converting it to a list or printing it), the database driver reports a syntax error in the SQL, pointing to the OVER keyword. In other words, the query fails at runtime with an operational error complaining about “near ‘OVER’: syntax error.” This happens because Django casts only the LAG expression itself to NUMERIC instead of casting the entire window call. SQLite rejects the resulting SQL. If you run the same query against the float field or explicitly set output_field=FloatField() on the Lag function, the query succeeds as expected.  

The generated SQL query is:  
SELECT "test1_lagtest"."id", "test1_lagtest"."modified", "test1_lagtest"."data",  
"test1_lagtest"."amount", CAST(LAG("test1_lagtest"."amount", 7) AS NUMERIC) OVER  
(PARTITION BY "test1_lagtest"."modified" ORDER BY "test1_lagtest"."modified" ASC)  
AS "w" FROM "test1_lagtest"  

I believe this fails as the CAST() statement ends after LAG whereas it should be around the whole statement up until "w".  
This only applies where the lagged field is a DecimalField; for example,  
w = Window(expression=Lag('data',7), partition_by=[F('modified')], order_by=F('modified').asc())  
works correctly.  
I can override it by adding output_field=FloatField() to the Lag function, for example:  
w = Window(expression=Lag('amount',7,output_field=FloatField()), partition_by=[F('modified')], order_by=F('modified').asc())