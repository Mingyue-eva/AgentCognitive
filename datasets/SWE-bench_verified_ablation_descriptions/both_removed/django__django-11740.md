Change uuid field to FK does not create dependency

Description

(last modified by Simon Charette)

Hi! I am new in django community, so please help me, because i really don’t know if this is a bug.

I have a Django project named “testproject” with two apps: testapp1 and testapp2. After some time I changed a UUIDField in testapp1 to a ForeignKey to App2, then created a new migration. The generated Migration class did not include any dependency on testapp2, despite the FK. I believe the migration should declare a dependency on testapp2.

This project uses Django 2.2 and PostgreSQL.  
Here is my post in django-users:  
https://groups.google.com/forum/#!searchin/django-users/Django%20bug%3A%20change%20uuid%20field%20to%20FK%20does%20not%20create%20dependency%7Csort:date/django-users/-h9LZxFomLU/yz-NLi1cDgAJ

Regards,  
Viktor Lomakin