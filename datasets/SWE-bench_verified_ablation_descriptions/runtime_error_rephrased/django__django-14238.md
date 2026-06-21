DEFAULT_AUTO_FIELD subclass check fails for subclasses of BigAutoField and SmallAutoField.
Description

Set DEFAULT_AUTO_FIELD = "example.core.models.MyBigAutoField", with contents of example.core.models:
from django.db import models
class MyBigAutoField(models.BigAutoField):
    pass
class MyModel(models.Model):
    pass
Django then crashes during model import, raising a ValueError that says the primary key "example.core.models.MyBigAutoField" referred to by DEFAULT_AUTO_FIELD must subclass AutoField.
This can be fixed in AutoFieldMeta.__subclasscheck__ by allowing subclasses of those classes in the _subclasses property.