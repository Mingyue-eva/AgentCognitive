Formsets' add_fields() method fails in some circumstances if the argument index is None.  
Description  

Formsets' add_fields() method fails in some circumstances if the argument index is None. When a FormSet has the attributes self.can_delete == True and self.can_delete_extra == False, calling the add_fields() method on that FormSet fails if the argument index is None. This occurs for example when calling FormSet.empty_form(). The result is that the method raises a TypeError indicating that it cannot compare a None value with an integer.  

Code example:  
To trigger this problem, you create a formset factory for your form class with deletion enabled but without allowing extra deletions. You then instantiate that formset without supplying any initial data and attempt to retrieve its empty_form. At that point, instead of returning an empty form instance, Django tries to compare a missing index (None) against the number of initial forms and raises a type error.  

The reason this happens is that in line 493 of django.forms.formsets index is compared to initial_form_count:  
if self.can_delete and (self.can_delete_extra or index < initial_form_count):  
Checking for index not None should fix the issue:  
if self.can_delete and (self.can_delete_extra or (index is not None and index < initial_form_count)):  

How to Reproduce  
You can reproduce this bug by writing a small standalone Django script. In that script, define a simple Form subclass with a single character field, configure Django settings programmatically, and create a formset factory for that form with can_delete set to true and can_delete_extra set to false. Instantiate the formset without any initial data and then try to access or print the empty_form attribute. At that moment, the code will fail with the same type error due to comparing None to an integer.