aggregate() with 'default' after annotate() crashes.

Description

I saw this on a PostgreSQL project and reproduced it with SQLite. Django 4.0.1.

Annotate (anything) then aggregate works fine, but adding the aggregate classes’ default argument (new in 4.0) breaks:

OperationalError: near "FROM": syntax error

The generated SQL:
'SELECT FROM (SELECT "core_book"."id" AS "idx", COALESCE(SUM("core_book"."id"), ?) AS "id__sum" FROM "core_book") subquery'
params: (0,)