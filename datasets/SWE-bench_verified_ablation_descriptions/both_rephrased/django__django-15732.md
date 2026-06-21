Cannot drop unique_together constraint on a single field with its own unique=True constraint

Description

Reproduction
If you define a Django model where the primary key field “id” is also listed in a unique_together constraint, then generate and apply a migration that is supposed to remove that unique_together entry, you will trigger the issue. You would expect the migration to drop the extra constraint on “id” and complete successfully.

Runtime error
When running the migration to remove the unique constraint, the migration framework looks for all unique indexes on the “id” column and finds two—one from the primary key and one from the former unique_together setting. Since it assumes there should only be a single unique index, it fails to remove the constraint.

Indexes:
    "foo_bar_pkey" PRIMARY KEY, btree (id)
    "foo_bar_id_1c3b3088c74c3b17_uniq" UNIQUE CONSTRAINT, btree (id)
Database is PostgreSQL, if that makes any difference.