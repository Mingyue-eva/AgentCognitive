Migrations uses value of enum object instead of its name.  
Description  
  
    (last modified by oasl)  
  
When using an Enum object as a default value for a CharField, the generated migration file uses the enum’s value instead of its name. This becomes a problem if that value is marked for translation, because once the translation changes the string, applying any existing migrations fails with a lookup error.  
  
Reproduction and expected behavior:  
Imagine you define an enum in your models.py like this:  

- You create a Status enum whose members GOOD and BAD wrap calls to gettext_lazy, so that “Good” and “Bad” get translated at runtime.  
- You then add a model field:  
  status = models.CharField(default=Status.GOOD, max_length=128)  

When you run makemigrations, Django emits a migration that hardcodes the enum’s translated value:  

    status = models.CharField(default=Status('Good'), max_length=128)  

Because “Good” is translated to different words in different locales, loading that migration later raises:  
ValueError: 'Good' is not a valid Status  

What you really want is for migrations to reference the enum member by name, which never changes. In other words, the migration should look like this:  

    status = models.CharField(default=Status['GOOD'], max_length=128)  

That way, regardless of any translation applied to the enum’s value, the migration will always find the member by its fixed name.