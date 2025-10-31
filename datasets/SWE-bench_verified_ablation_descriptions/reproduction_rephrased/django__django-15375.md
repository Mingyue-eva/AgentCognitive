aggregate() with 'default' after annotate() crashes.  
Description  

I saw this on a PostgreSQL project and reproduced it with SQLite on Django 4.0.1. I opened the Django shell under Python 3.10.2 (IPython 7.30.1), imported the ORM functions and my Book model, and confirmed there are 95 books in the database. Next, I annotated each book with its id (using F('id') as “idx”) and called aggregate(Sum('id')); this returned 4560 as expected. I also verified that using Coalesce(Sum('id'), 0) in the aggregate produces the correct total of 4560. However, as soon as I add the new default argument to Sum, the query fails:

In [6]: Book.objects.annotate(idx=F("id")).aggregate(Sum("id", default=0))  
---------------------------------------------------------------------------  
OperationalError                         Traceback (most recent call last)  
...  
OperationalError: near "FROM": syntax error  
The generated SQL:  
In [7]: %debug  
> /.../django/db/backends/sqlite3/base.py(416)execute()  
    414             return Database.Cursor.execute(self, query)  
    415         query = self.convert_query(query)  
--> 416         return Database.Cursor.execute(self, query, params)  
    417  
    418     def executemany(self, query, param_list):  
ipdb> query  
'SELECT FROM (SELECT "core_book"."id" AS "idx", COALESCE(SUM("core_book"."id"), ?) AS "id__sum" FROM "core_book") subquery'  
ipdb> params  
(0,)  
ipdb>