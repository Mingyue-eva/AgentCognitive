Django Admin with Inlines not using UUIDField default value  
Description  
     
    (last modified by Joseph Metzinger)  
     
Hello,  
I am a long time django user, first time bug reporter, so please let me know if I need to do anything else to help get this bug fixed :)  

I’m working with Django 3.1.3 on Python 3.8.5 and created a minimal project to demonstrate the problem. In it, there’s an abstract base model that defines a BigAutoField primary key and a UUIDField defaulting to uuid.uuid4, and then a concrete Thing model that inherits from it. A SubThing model holds a foreign key to Thing, pointing at the UUIDField. In the admin, Thing is registered with a stacked inline for SubThing.  

If you log into the admin, remove all existing SubThing entries, enter a name for a Thing, and save, everything works as expected. However, the moment you try to add a SubThing on the same form when creating or editing a Thing, saving the form triggers an exception:  

https://dpaste.com/8EU4FF6RW  

It shows that the value of "id" in the Thing model is being set to null.  
I believe this is a bug in django.  
Thanks!