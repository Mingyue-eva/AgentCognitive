Missing import statement in generated migration (NameError: name 'models' is not defined)

Description

I found a bug in Django's latest release: 3.2.4.

To reproduce the issue, define a custom text field subclass, an abstract base model, and a simple mixin in your app’s models, then create a concrete model that combines the mixin and the abstract base and uses the custom field as its primary key. When you run the makemigrations command, you expect Django to emit a migration file that includes valid imports for all referenced classes.

In practice, the generated migration file only pulls in the application’s models module and the migrations framework, but omits the import for django.db.models. As soon as you try to apply or import this migration, Python raises a NameError because it encounters a reference to models.Model without having imported that name. This indicates the migration file is not valid Python code.

Expected behavior: Django generates a migration file that is valid Python.  
Actual behavior: Django generates a migration file that is missing an import statement.

I think this is a bug of the module django.db.migrations.writer, but I'm not sure. I will be happy to assist with debugging.  
Thanks for your attention,  
Jaap Joris