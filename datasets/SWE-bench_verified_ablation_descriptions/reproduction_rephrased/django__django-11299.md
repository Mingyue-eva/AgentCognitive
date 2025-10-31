Description
     
    (last modified by Michael Spallino)
     
Django is incorrectly including the fully qualified field name (e.g. “my_table”.”my_field”) in part of the check constraint. This only appears to happen when there is a combination of OR and AND clauses in the CheckConstraint. Including the fully qualified field name fails the migration because when we drop the old table and swap the name of the staging table in place, the constraint fails with a malformed schema exception (on sqlite) saying that the field doesn’t exist on the table. It appears that this has to do with the AND clause items using Col while the OR clause uses SimpleCol.

For example, suppose we have a model TestConstraint with two fields: an integer field_1 that allows nulls and a non-nullable boolean flag. We add a CheckConstraint that enforces “either flag is true and field_1 is not null, or flag is false.” When Django generates and applies the migration on SQLite, it creates a temporary table named new__app_testconstraint containing the same columns plus that constraint. Due to an internal bug, the first part of the OR condition is rendered with explicit table qualifiers—new__app_testconstraint.field_1 IS NOT NULL AND new__app_testconstraint.flag = 1—while the second part remains unqualified as flag = 0. After copying the data over and attempting to rename the staging table back to the original name, SQLite rejects the change because it cannot find a column called new__app_testconstraint.field_1.

The ALTER TABLE fails with the following: 
malformed database schema (app_testconstraint) - no such column: new__app_testconstraint.field_1.

By contrast, the constraint should be generated so that both sides of the OR clause reference the columns without any table prefixes—for example, CHECK ((field_1 IS NOT NULL AND flag = 1) OR flag = 0).