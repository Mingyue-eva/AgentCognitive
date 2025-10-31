Migration crashes deleting an index_together if there is a unique_together on the same fields  
Description  
  
Happens with Django 1.11.10  
Steps to reproduce:  
1) Create models with 2 fields, add those same fields to both unique_together and index_together  
2) Delete index_together → Fail  
When running the migration, Django raises a ValueError because it finds two matching constraints—the unique constraint and the index—where it expected only one, so it cannot decide which one to remove.  
The worst in my case is that it happened as I wanted to refactor my code to use the new Options.indexes feature in Django 1.11. I am actually not deleting the index itself, just changing how it’s declared in my code.  
I think there are two separate issues here:  
1) Deleting index_together should be allowed on its own or made coherent with unique_together in migrations  
2) Moving the declaration of an index should not trigger an index recreation