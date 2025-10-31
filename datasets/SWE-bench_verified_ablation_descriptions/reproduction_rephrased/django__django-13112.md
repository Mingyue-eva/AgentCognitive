makemigrations crashes for ForeignKey with mixed-case app name.

Description

I have a Django project where I registered an application called “DJ_RegLogin” by adding it to INSTALLED_APPS in settings.py. In the app’s apps.py I defined an AppConfig with name 'DJ_RegLogin' and verbose_name “Contents.” Inside models.py I created a Category model with title and slug fields, and a Content model that includes various fields such as title, slug, body, posted date, sites, ip address, status, plus two ForeignKeys—one to Category and another to User. This configuration works under Django 3.0, but when I run:

    python3 manage.py migrate

on Django 3.1b1, I get the following error:

ValueError: The field DJ_RegLogin.Content.category was declared with a lazy reference to 'dj_reglogin.category', but app 'dj_reglogin' isn't installed.