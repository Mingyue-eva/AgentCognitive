aggregate() with 'default' after annotate() crashes.

Description

I saw this on a PostgreSQL project and reproduced it with SQLite. Django 4.0.1. Annotate then aggregate works fine, but adding the aggregate classes’ default argument (new in 4.0) breaks. The long form using Coalesce works as expected.