admin.E108 is raised on fields accessible only via instance.
Description

(last modified by ajcsimons)

As part of startup Django validates the ModelAdmin’s list_display list/tuple for correctness (django.admin.contrib.checks._check_list_display). Having upgraded Django from 2.0.7 to 2.2.1 I found that a ModelAdmin with a list_display that used to pass the checks and work fine in admin now fails validation, preventing Django from starting. A PositionField from the django-positions library triggers this bug, explanation why follows.

from django.db import models  
from position.Fields import PositionField  
class Thing(models.Model):  
    number = models.IntegerField(default=0)  
    order = PositionField()  

from django.contrib import admin  
from .models import Thing  
@admin.register(Thing)  
class ThingAdmin(admin.ModelAdmin):  
    list_display = ['number', 'order']  

When running under Django 2.2.1, startup fails because the admin check incorrectly rejects the 'order' entry in list_display, claiming that it is neither a callable, nor an attribute of the ThingAdmin class, nor a field or method on the Thing model, and raises admin.E108. Under Django 2.0.7 the same configuration passes validation and the site starts normally.  

If you change 'number' to 'no_number' or 'order' to 'no_order' then the validation correctly complains about those.

The reason for this bug is commit https://github.com/django/django/commit/47016adbf54b54143d4cf052eeb29fc72d27e6b1 which was proposed and accepted as a fix for bug https://code.djangoproject.com/ticket/28490. The problem is while it fixed that bug it broke the functionality of _check_list_display_item in other cases. The rationale for that change was that after field=getattr(model, item) field could be None if item was a descriptor returning None, but subsequent code incorrectly interpreted field being None as meaning getattr raised an AttributeError. As this was done after trying field = model._meta.get_field(item) and that failing that meant the validation error should be returned. However, after the above change if hasattr(model, item) is false then we no longer even try field = model._meta.get_field(item) before returning an error. The reason hasattr(model, item) is false in the case of a PositionField is its get method throws an exception if called on an instance of the PositionField class on the Thing model class, rather than a Thing instance.

For clarity, here are the various logical tests that _check_list_display_item needs to deal with and the behaviour before the above change, after it, and the correct behaviour (which my suggested patch exhibits). Note this is assuming the first 2 tests callable(item) and hasattr(obj, item) are both false (corresponding to item is an actual function/lambda rather than string or an attribute of ThingAdmin).  
[logical tests table omitted]

The following code exhibits the correct behaviour in all cases. The key changes are there is no longer a check for hasattr(model, item), as that being false should not prevent us from attempting to get the field via get_field, and only return an E108 in the case both of them fail. If either of those means of procuring it are successful then we need to check if it’s a ManyToMany. Whether or not the field is None is irrelevant, and behaviour is contained within the exception catching blocks that should cause it instead of signalled through a variable being set to None which is a source of conflation of different cases.

def _check_list_display_item(self, obj, item, label):
    if callable(item):
        return []
    elif hasattr(obj, item):
        return []
    else:
        try:
            field = obj.model._meta.get_field(item)
        except FieldDoesNotExist:
            try:
                field = getattr(obj.model, item)
            except AttributeError:
                return [
                    checks.Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute or method on '%s.%s'." % (
                            label, item, obj.__class__.__name__,
                            obj.model._meta.app_label, obj.model._meta.object_name,
                        ),
                        obj=obj.__class__,
                        id='admin.E108',
                    )
                ]
        if isinstance(field, models.ManyToManyField):
            return [
                checks.Error(
                    "The value of '%s' must not be a ManyToManyField." % label,
                    obj=obj.__class__,
                    id='admin.E109',
                )
            ]
        return []