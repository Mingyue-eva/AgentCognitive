## Issue Description  
The value of a TextChoices/IntegerChoices field has a differing type  

Description  
If we create an instance of a model having a CharField or IntegerField with the keyword choices pointing to IntegerChoices or TextChoices, the value returned by the getter of the field will be of the same type as the one created by enum.Enum (enum value).  

For example, imagine you define a TextChoices enum named MyChoice with two options, FIRST_CHOICE mapped to the string "first" and SECOND_CHOICE mapped to "second". You then create a Django model MyObject that uses this enum for a CharField called my_str_value.  

Reproduction steps and expected behavior:  
• Use the Django ORM to create a MyObject record, assigning the FIRST_CHOICE enum member to my_str_value.  
• Immediately after creation, inspect my_str_value. You expect it to be a plain Python string and, if you convert it to a string, to get "first".  
• Next, fetch the same record from the database (for example, via MyObject.objects.last()) and perform the same checks: you expect the attribute to still be a plain string and its string conversion to be "first".  

Runtime error observed:  
When running the Django test suite that performs these checks, the assertion for the freshly created instance fails. Instead of receiving the raw string "first", the field’s getter returns an enum member whose string representation is "MyChoice.FIRST_CHOICE". This discrepancy leads to an unexpected test failure.  

We notice when invoking __str__(...) we don't actually get the value property of the enum value which can lead to some unexpected issues, especially when communicating to an external API with a freshly created instance that will send MyEnum.MyValue, and the one that was retrieved would send my_value.