Formsets’ add_fields() method fails in some circumstances if the argument index is None.

Description

Formsets’ add_fields() method fails in some circumstances if the argument index is None. When a FormSet has the attributes self.can_delete == True and self.can_delete_extra == False, calling the add_fields() method on that FormSet fails if the argument index is None. This occurs for example when calling FormSet.empty_form(). The result is that the method raises the exception TypeError: '<' not supported between instances of 'NoneType' and 'int'. 

Code example

For instance, you might define a formset factory for a simple form (MyForm) with deletion enabled but extra-deletion disabled, then instantiate it without any initial data and immediately request its empty_form. Internally, add_fields() is invoked with index=None, triggering the following error:

TypeError: '<' not supported between instances of 'NoneType' and 'int'

The reason this happens is that in line 493 of django/forms/formsets.py index is compared to initial_form_count:
if self.can_delete and (self.can_delete_extra or index < initial_form_count):
Checking for index not None should fix the issue:
if self.can_delete and (self.can_delete_extra or (index is not None and index < initial_form_count)):

How to Reproduce

In a minimal Django setup, you can reproduce this by:
- Configuring basic settings (DEBUG=True, an empty MIDDLEWARE_CLASSES, and a valid ROOT_URLCONF).
- Defining a simple Form subclass with a single CharField.
- Creating a formset factory for that form with can_delete=True and can_delete_extra=False.
- Instantiating the formset with initial=None.
- Accessing the empty_form property, which causes add_fields(None) to run and raises the TypeError '<' not supported between instances of 'NoneType' and 'int'.