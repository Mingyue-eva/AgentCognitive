makemigrations crashes for ForeignKey with mixed-case app name.

On Django 3.1b1, migrations fail because a ForeignKey to Category references ‘dj_reglogin.category’, but the app is installed as ‘DJ_RegLogin’. In Django 3.0 this configuration worked without issues. The INSTALLED_APPS entry and AppConfig both use the mixed-case ‘DJ_RegLogin’.