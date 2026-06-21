__in doesn’t clear selected fields on the RHS when QuerySet.alias() is used after annotate().

Description

To reproduce the bug, write a test that:
1. Filters Book records to those with more than 400 pages.
2. Calls annotate() to add a constant field named book_annotate.
3. Calls alias() to add another constant field named book_alias.
4. Uses that QuerySet in Publisher.objects.filter(book__in=...) and then calls values("name") to retrieve only publisher names.
5. Asserts that the returned names are exactly Apress, Sams, Prentice Hall, and Morgan Kaufmann.

You should get this error:
django.db.utils.OperationalError: sub-select returns 10 columns - expected 1