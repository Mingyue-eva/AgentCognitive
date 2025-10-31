Change uuid field to FK does not create dependency  
Description  
  
(last modified by Simon Charette)  
  
Hi! I am new in django community, so please help me, because i really dont know is it really "bug".  
I have a django project named "testproject" and two apps: testapp1, testapp2.  
It will be simpler to understand, with this example:  
  
Initially, the first app defined a model named App1 with a UUID primary key and a separate UUID field called another_app, intended to hold the identifier of the second app’s model. The second app defined a model named App2, also with a UUID primary key. After some time, I changed the App1 model so that the plain UUID field was replaced by a foreign key to App2, using SET_NULL for deletions. When I generated a new migration, the migration file was created without any dependency entry for testapp2, even though a foreign key now points to it. I expected the migration to declare a dependency on the second app.  
  
This project uses Django version 2.2 and PostgreSQL. I have attached an archive with sources. When I run the provided test suite, it fails because the migration process cannot locate the referenced model in testapp2, causing the tests to abort before completion.  
  
So is it a problem in Django or am I missing something?  
Here is my post in django users:  
https://groups.google.com/forum/#!searchin/django-users/Django$20bug$3A$20change$20uuid$20field$20to$20FK$20does$20not$20create$20dependency%7Csort:date/django-users/-h9LZxFomLU/yz-NLi1cDgAJ  
Regards, Viktor Lomakin