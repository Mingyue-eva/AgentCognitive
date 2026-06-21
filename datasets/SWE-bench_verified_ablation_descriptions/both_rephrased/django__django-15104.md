KeyError with migration autodetector and FK field with hardcoded reference  
Description  

Hi,  
I encountered this issue on an old Django project (probably 10 years old) with tons of models and probably a lot of questionable design decisions.  
The symptom is that running our test suite in verbose mode doesn’t work:  
$ python manage.py test -v 2  
Creating test database for alias 'default' ('test_project')…  
Operations to perform:  
  Synchronize unmigrated apps: [… about 40 apps]  
  Apply all migrations: (none)  
Synchronizing apps without migrations:  
  Creating tables…  
    Creating table auth_permission  
    Creating table auth_group  
    …  
  Running deferred SQL…  
Running migrations:  
  No migrations to apply.  

At that point, when Django’s migration autodetector moves on to detect any changes it crashes with a KeyError for ‘to’. During the phase where it inspects each model’s field definitions, it tries to delete a ‘to’ entry that isn’t present and Python raises the exception.

I finally did some digging and found that the culprit is a custom ForeignKey field that hardcodes its to argument (and thus also removes it from its deconstructed kwargs). It seems that the autodetector doesn’t like that.

Here’s how I reproduced the issue in a minimal test case:  
I defined a subclass of ForeignKey whose constructor always sets the related model to a fixed string and whose deconstruct method removes the ‘to’ key from its keyword arguments. Then I built two in‐memory project states: the first contained only the target model, and the second added a new model with a field using this custom foreign key. When I passed those two states to Django’s MigrationAutodetector and asked it to generate changes, I expected to see exactly one change (the new model addition), but instead it blew up with a KeyError during change detection.

While I’ll happily admit that my custom field’s design might be questionable, I don’t think it’s incorrect and I think the autodetector is at fault here.  
Changing `del deconstruction[2]['to']` to `deconstruction[2].pop('to', None)` on the line indicated by the traceback makes my test suite run again, in all its glorious verbosity. Seems like an innocent enough fix to me.