Change uuid field to FK does not create dependency  
Description  
     
    (last modified by Simon Charette)  
     
Hi! I am new in django community, so please help me, because i really dont know is it really "bug".  
I have a Django project named "testproject" that includes two apps, testapp1 and testapp2. In testapp1 I originally defined an App1 model with a UUIDField as primary key, a CharField for text, and another_app as a nullable, blankable UUIDField. In testapp2 I defined an App2 model also using a UUIDField primary key and a text CharField.  
Afterwards I changed the another_app field on App1 to a ForeignKey to App2 (null=True, blank=True, on_delete=models.SET_NULL). When I ran makemigrations, the new migration did not include testapp2 in its dependencies even though App1.another_app now refers to App2. I expected the migration to automatically add a dependency on testapp2.  
This project uses Django 2.2 and PostgreSQL. I included a minimal test in the repo that, when run, raises the following exception:  
ValueError: Related model 'testapp2.App2' cannot be resolved.  
So is this a problem in Django, or am I misunderstanding something?  
Here is my post in django users:  
https://groups.google.com/forum/#!searchin/django-users/Django%20bug%3A%20change%20uuid%20field%20to%20FK%20does%20not%20create%20dependency%7Csort:date/django-users/-h9LZxFomLU/yz-NLi1cDgAJ  
Regards, Viktor Lomakin