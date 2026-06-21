QuerySet.only() after select_related() crash on proxy models.

Description

On Windows 10 with Python 3.10 and Django 4.0.5, I defined a base model with a name field and a proxy subclass, plus another model that holds a ForeignKey to that proxy. I then wrote a Django management command that fetches all instances of the second model by first calling select_related("custom") to follow the proxy relation and then only("custom__name") to limit the selected columns to the related model’s name before converting the queryset to a list. I expected to get back a list of objects with only the related name field loaded, but instead the query raises an error indicating that the primary key "id" is missing from the selected fields.

Models:
class CustomModel(models.Model):
    name = models.CharField(max_length=16)

class ProxyCustomModel(CustomModel):
    class Meta:
        proxy = True

class AnotherModel(models.Model):
    custom = models.ForeignKey(
        ProxyCustomModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

I implemented a custom management command that triggers the issue by retrieving all AnotherModel objects with select_related("custom") followed by only("custom__name") and then forcing evaluation with list().

At django/db/models/sql/query.py in 745 line there is snippet:
opts = cur_model._meta

If I replace it by 
opts = cur_model._meta.concrete_model._meta
all works as expected.