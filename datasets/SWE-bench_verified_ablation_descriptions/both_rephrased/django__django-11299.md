CheckConstraint with OR operator generates incorrect SQL on SQLite and Oracle.

Description  
(last modified by Michael Spallino)

Django is incorrectly including the fully qualified field name (for example “my_table”.“my_field”) in part of the check constraint definition. This only appears to happen when there is a combination of OR and AND clauses in the CheckConstraint. Including the fully qualified field name causes the migration to fail because, when Django drops the old table and renames the staging table into place, the constraint refers to a column name that no longer exists under that fully qualified name.

Reproduction  
Define a Django model with two fields—an integer field that may be null and a boolean flag that is always required—and add a CheckConstraint that enforces “if the flag is true then the integer field must not be null, otherwise the flag must be false.” Generate and apply a migration for this model. During the migration, Django creates a new temporary table and defines the check constraint. However, the generated CREATE TABLE statement embeds the staging table’s name in only one part of the constraint, while leaving the other part unqualified. When Django then attempts to rename the temporary table over the existing one, the database complains that the referenced column cannot be found under the qualified name.

Runtime Error  
When the migration reaches the step that renames the staging table to the target table name, the database engine reports a malformed schema and rejects the operation. It indicates that the column reference using the staging table’s name does not exist, causing the ALTER TABLE (RENAME) step to fail.

Expected Behavior  
The CREATE TABLE statement for the staging table should define the check constraint without any table name qualification in either the AND or the OR clause. In other words, both sides of the condition should refer simply to “field_1” and “flag,” so that the table can be renamed successfully.