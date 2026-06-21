RenameIndex() crashes when unnamed index is moving backward and forward.  
Description

RenameIndex() should restore the old auto-generated name when an unnamed index for unique_together is moving backward. Now re-applying RenameIndex() crashes. For example:  
In a migration test subclass, we first open a schema editor and run the backwards migration, then verify that an index called "new_pony_test_idx" appears on the table. Next, we open a fresh schema editor, run the forwards migration, and again check that the same index name exists. Finally, we deconstruct the RenameIndex operation and confirm its name is still "RenameIndex".

crashes on PostgreSQL:  
django.db.utils.ProgrammingError: relation "new_pony_test_idx" already exists