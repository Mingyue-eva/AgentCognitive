Change uuid field to FK does not create dependency  
Description  
(last modified by Simon Charette)  

Hi! I am new in the Django community, so please help me, because I really don’t know if this is a “bug.” I have a Django project using version 2.2 and PostgreSQL. I changed a UUIDField to a ForeignKey, created a new migration, but the Migration class did not add any dependencies for the related app. I believe it should, because of the FK.  

After running the project I get this runtime error:  
ValueError: Related model 'testapp2.App2' cannot be resolved.  

So is this a problem in Django or am I misunderstanding something?  
Here is my post in django-users:  
https://groups.google.com/forum/#!searchin/django-users/Django$20bug$3A$20change$20uuid$20field$20to$20FK$20does$20not$20create$20dependency%7Csort:date/django-users/-h9LZxFomLU/yz-NLi1cDgAJ  

Regards,  
Viktor Lomakin