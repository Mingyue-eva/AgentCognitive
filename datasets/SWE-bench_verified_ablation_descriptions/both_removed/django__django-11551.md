admin.E108 is raised on fields accessible only via instance.

Description  
As part of startup, Django validates the ModelAdmin’s list_display for correctness. After upgrading from Django 2.0.7 to 2.2.1, a ModelAdmin that previously passed validation now fails with an incorrect admin.E108 when using a PositionField from django-positions. Under 2.0.7 the same configuration started successfully, and if truly invalid field names are used the validation still correctly complains.

Root cause  
A commit intended to fix ticket 28490 introduced an early hasattr(model, item) check in _check_list_display_item. When hasattr(model, item) is false, get_field(item) is never attempted and E108 is raised prematurely. PositionField’s descriptor throws an exception when accessed on the model class, causing hasattr to return false and trigger the incorrect error.

Correct logic  
If callable(item) or hasattr(obj, item) is true, no errors should be raised. Otherwise, the code should first try model._meta.get_field(item), and only if that raises FieldDoesNotExist then try getattr(obj.model, item). An E108 should be returned only if both attempts fail; an E109 should be returned if the obtained field is a ManyToManyField.