Migration crashes deleting an index_together if there is a unique_together on the same fields

Happens with Django 1.11.10

When attempting to delete index_together on fields also in unique_together, the migration fails.

In my case this occurred while refactoring to use the new Options.indexes feature, not deleting the index but changing its declaration.

I think there are 2 different points here:
1) The deletion of index_together should be possible independently or made coherent with unique_together migrations.
2) Moving the declaration of an index should not result in index re-creation.