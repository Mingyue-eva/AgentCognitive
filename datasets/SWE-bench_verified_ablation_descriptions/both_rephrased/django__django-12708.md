Migration crashes deleting an index_together if there is a unique_together on the same fields

Description

Happens with Django 1.11.10

Reproduction
First you define a model with two fields and list those same fields in both unique_together and index_together. Next you remove the index_together entry from the model and run makemigrations followed by migrate. You expect the migration to drop the index and complete successfully.

Runtime error
During the migration that deletes the index, Django tries to identify the constraint to remove but finds two constraints on the same fields: the unique constraint and the index constraint. Unable to distinguish between them, it raises a ValueError and stops the migration.

The worst in my case is that happened as I wanted to refactor my code to use the "new" (Dj 1.11) Options.indexes feature. I am actually not deleting the index, just the way it is declared in my code.  
I think there are 2 different points here:  
1) The deletion of index_together should be possible alone or made coherent (migrations side?) with unique_together  
2) Moving the declaration of an index should not result in an index re-creation