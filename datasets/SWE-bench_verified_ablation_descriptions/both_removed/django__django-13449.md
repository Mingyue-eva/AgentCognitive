Lag() with DecimalField crashes on SQLite.

On Django 3.0.7 with a SQLite database, annotating a Window expression using Lag() on a DecimalField results in a syntax error because the CAST() is applied only to the LAG() call rather than the entire OVER clause. This issue does not occur with non-DecimalField fields, and specifying output_field=FloatField() on Lag() works around the problem.