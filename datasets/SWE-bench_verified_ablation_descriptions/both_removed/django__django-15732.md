Cannot drop unique_together constraint on a single field with its own unique=True constraint

I have an erroneous unique_together constraint on a model’s primary key that cannot be dropped by a migration. The migration tries to find all unique constraints on the column and expects there to be only one, but I have both the primary key and the unique_together constraint.

Database is PostgreSQL, if that makes any difference.