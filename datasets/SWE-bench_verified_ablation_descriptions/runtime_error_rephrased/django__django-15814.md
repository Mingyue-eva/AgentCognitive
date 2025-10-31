QuerySet.only() after select_related() crash on proxy models.

Description

When I optimize a query using select_related() and only() methods from the proxy model I encounter an error: Windows 10; Python 3.10; Django 4.0.5. When the management command runs the query with select_related("custom") and only("custom__name"), Django tries to populate the related proxy model but doesn’t include its primary key in the selected fields, so it raises a ValueError stating that 'id' is not in the list.

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

Command:
class Command(BaseCommand):
    def handle(self, *args, **options):
        list(AnotherModel.objects.select_related("custom").only("custom__name").all())

At django/db/models/sql/query.py in 745 line there is snippet:
opts = cur_model._meta
If I replace it by 
opts = cur_model._meta.concrete_model._meta
all works as expected.