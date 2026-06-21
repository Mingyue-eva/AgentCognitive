DEFAULT_AUTO_FIELD subclass check fails for subclasses of BigAutoField and SmallAutoField.

Description

If you configure Django’s DEFAULT_AUTO_FIELD setting to point at your own subclass of BigAutoField and then define that subclass in your app’s models module, you can trigger the problem simply by declaring a model without its own primary key and starting the application (for example, by running any management command). You would expect Django to recognize your custom field as a valid default primary key type and load normally.

Instead, when Django imports your models and prepares their options, it stops with an error saying that the class you named in DEFAULT_AUTO_FIELD must subclass AutoField. Even though your custom field does inherit from BigAutoField, Django’s internal subclass check does not accept it and the initialization fails.

This can be fixed in AutoFieldMeta.__subclasscheck__ by allowing subclasses of those classes in the _subclasses property.