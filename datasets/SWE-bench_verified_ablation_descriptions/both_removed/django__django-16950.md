Django Admin with Inlines not using UUIDField default value

Description

I am a long time Django user and using Django 3.1.3 with Python 3.8.5. I have an abstract base model that provides an auto primary key and a UUIDField(default=uuid.uuid4). I created a concrete Thing model and a SubThing model with a ForeignKey to the Thing’s UUIDField, and I registered Thing in the admin with a StackedInline for SubThing.

When creating a Thing together with a SubThing inline in the admin, the UUIDField default on Thing is not applied and the id ends up null. I believe this is a bug in Django.

Thanks!