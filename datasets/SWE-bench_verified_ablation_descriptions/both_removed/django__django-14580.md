Missing import statement in generated migration (NameError: name 'models' is not defined)

Description

I found a bug in Django’s latest release, 3.2.4. When running makemigrations for a model that uses a custom field and mixin, the generated migration imports the app’s models module but omits the import of django.db.models. As a result, the migration file references models.Model without importing it.

Expected behavior: Django generates a migration file that is valid Python.

Actual behavior: Django generates a migration file that is missing an import statement.

I think this is a bug in django.db.migrations.writer, but I’m not sure. I will be happy to assist with debugging.

Thanks for your attention,
Jaap Joris