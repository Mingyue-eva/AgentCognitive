Missing import statement in generated migration (NameError: name 'models' is not defined)

Description

I found a bug in Django’s latest release: 3.2.4.

To reproduce this issue, create a Django app whose models.py defines:
- a custom TextField subclass,
- an abstract base model,
- a simple mixin class,
- and a concrete model that inherits from the mixin and the abstract base, using the custom field as its primary key.

When you run the makemigrations command, Django will emit a migration file that imports only your app’s models module and django.db.migrations, but never imports django.db.models. In that migration’s CreateModel operation, the bases tuple ends up as (app.models.MyMixin, models.Model), so the file is syntactically invalid Python.

Which will then fail with the following error:
 File "/home/jj/django_example/app/migrations/0001_initial.py", line 7, in <module>
     class Migration(migrations.Migration):
 File "/home/jj/django_example/app/migrations/0001_initial.py", line 23, in Migration
     bases=(app.models.MyMixin, models.Model),
 NameError: name 'models' is not defined

Expected behavior: Django generates a migration file that is valid Python.  
Actual behavior: Django generates a migration file that is missing an import statement.

I think this is a bug of the module django.db.migrations.writer, but I’m not sure. I will be happy to assist with debugging.  
Thanks for your attention,  
Jaap Joris