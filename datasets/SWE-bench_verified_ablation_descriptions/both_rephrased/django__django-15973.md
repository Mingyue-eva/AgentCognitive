Defining the "through" model in a many-to-many field in another app causes "AttributeError: 'str' object has no attribute '_meta'" on migration

Description

I tried migrating my apps into the database, the three relevant apps are called: "fonte", "fonte_variavel" and "variavel". fonte and variavel models have a many-to-many relationship (field being defined on "fonte"). The many-to-many field uses fonte_variavel model as the "through" argument.

Reproduction:
To trigger this issue, create three separate Django apps: fonte, variavel, and fonte_variavel. In the fonte app define a model with a unique text field for name, another for description, date fields for a start date and an optional end date, and a many-to-many field called variaveis that points to the variavel app’s model via an intermediary model declared in the fonte_variavel app. In the variavel app define a model with a unique name and a description. In the fonte_variavel app define a model containing foreign keys to both the FonteModel and the VariavelModel. Generate and apply the migration for the fonte app. You should expect the migration to create both the Fonte table and the join table for the many-to-many relationship without errors.

Runtime Error:
When running the migration command, Django aborts the operation because it interprets the reference to the through model as a simple string instead of a model class. This results in an AttributeError indicating that a 'str' object has no attribute '_meta' at the moment Django attempts to build the database schema for the models. The migration fails and no tables are created.

If I move the FonteVariavelModel into the fonte app’s models file, the migration succeeds. Consolidating all models into a single file also avoids the error.