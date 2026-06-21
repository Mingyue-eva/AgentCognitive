## Issue Description  
Cannot drop unique_together constraint on a single field with its own unique=True constraint  

Description

I accidentally added a unique_together constraint on the primary key by setting  
```python
unique_together = (('id',),)
```  
When I run the migration intended to remove that constraint, it fails because the migration code expects only one unique index on the `id` column but finds two—the primary key and the extra unique_together index. In PostgreSQL, the table currently has these indexes:  
    "foo_bar_pkey" PRIMARY KEY, btree (id)  
    "foo_bar_id_1c3b3088c74c3b17_uniq" UNIQUE CONSTRAINT, btree (id)  

Database is PostgreSQL, if that makes any difference.