RenameIndex() crashes when unnamed index is moving backward and forward.

Description

RenameIndex() should restore the old auto-generated name when an unnamed index for unique_together is moving backward. Now re-applying RenameIndex() crashes. For example:

tests/migrations/test_operations.py
diff --git a/tests/migrations/test_operations.py b/tests/migrations/test_operations.py
index cfd28b1b39..c0a55023bb 100644
--- a/tests/migrations/test_operations.py
+++ b/tests/migrations/test_operations.py
@@ class OperationTests(OperationTestBase):
     with connection.schema_editor() as editor, self.assertNumQueries(0):
         operation.database_backwards(app_label, editor, new_state, project_state)
     self.assertIndexNameExists(table_name, "new_pony_test_idx")
     # Re-apply renaming.
     with connection.schema_editor() as editor:
         operation.database_forwards(app_label, editor, project_state, new_state)
     self.assertIndexNameExists(table_name, "new_pony_test_idx")
     # Deconstruction.
     definition = operation.deconstruct()
     self.assertEqual(definition[0], "RenameIndex")

Reproduction
To reproduce the problem, run the backward migration for the RenameIndex operation on the table with a unique_together index that has no explicit name. This will restore the index’s original generated name. Then, without altering the schema further, run the forward migration again to apply RenameIndex. Because the index already exists under the new name, the second migration attempt will fail.

Runtime Error
On PostgreSQL, the database reports an error indicating that an index with the target name already exists, causing the RenameIndex operation to abort.