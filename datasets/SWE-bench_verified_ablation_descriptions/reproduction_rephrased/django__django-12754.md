FieldError when migrating field to new model subclass.  
Description  

Analogous to #21890. If creating a model subclass and moving a field onto it in the same step, makemigrations works but migrate dies with django.core.exceptions.FieldError: Local field 'title' in class 'Book' clashes with field of the same name from base class 'Readable'.  

Reproduction steps:  
- Start with a model Readable that defines a title CharField.  
- Change the definition so that Readable no longer declares title, and introduce a subclass Book that declares title instead.  
- Run makemigrations; you’ll see a migration that first creates Book, then removes title from Readable.  
- Apply the migration with migrate and observe the FieldError below.  
- If you manually reverse those two operations in the migration file—removing title from Readable before creating Book—the migration applies successfully. Ideally the autodetector would choose that order.  

django.core.exceptions.FieldError: Local field 'title' in class 'Book' clashes with field of the same name from base class 'Readable'.