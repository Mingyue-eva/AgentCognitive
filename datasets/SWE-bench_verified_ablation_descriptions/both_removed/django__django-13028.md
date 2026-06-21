Queryset raises NotSupportedError when RHS has filterable=False attribute.

Description

(last modified by Nicolas Baccelli)

I'm migrating my app to Django 3.0.7 and I hit a strange behavior using a model class with a field labeled filterable:

class ProductMetaDataType(models.Model):
    label = models.CharField(max_length=255, unique=True)
    filterable = models.BooleanField(default=False, verbose_name=_("filterable"))
    class Meta:
        app_label = "adminpricing"
        verbose_name = _("product meta data type")
        verbose_name_plural = _("product meta data types")
    def __str__(self):
        return self.label

class ProductMetaData(models.Model):
    id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Produit, on_delete=models.CASCADE)
    value = models.TextField()
    marketplace = models.ForeignKey(Plateforme, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now, null=True)
    metadata_type = models.ForeignKey(ProductMetaDataType, on_delete=models.CASCADE)
    class Meta:
        app_label = "adminpricing"
        verbose_name = _("product meta data")
        verbose_name_plural = _("product meta datas")

Using a field named filterable in query filters leads to a NotSupportedError. Renaming the field to something else resolves the issue. This should be documented or fixed.