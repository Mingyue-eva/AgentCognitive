QuerySet.only() after select_related() crash on proxy models.

When I optimize a query using select_related() and only() methods from the proxy model I encounter an error.

Environment: Windows 10; Python 3.10; Django 4.0.5

At django/db/models/sql/query.py in line 745 there is a snippet:
opts = cur_model._meta
If I replace it by
opts = cur_model._meta.concrete_model._meta
all works as expected.