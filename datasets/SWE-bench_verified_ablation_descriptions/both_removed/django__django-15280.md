Deferred fields incorrect when following prefetches back to the "parent" object

Description

Given the following models:
class User(models.Model):
    email = models.EmailField()
    kind = models.CharField(
        max_length=10, choices=[("ADMIN", "Admin"), ("REGULAR", "Regular")]
    )
class Profile(models.Model):
    full_name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

When querying with User.objects.only("email") and prefetching Profile along with a nested prefetch on Profile’s User limited to only("kind"), accessing kind on the nested User still results in a database query. get_deferred_fields() for the inner User shows that "kind" was deferred correctly, suggesting Django is incorrectly inheriting deferred fields from the outer User queryset.

The same behavior occurs if the relationship is a ForeignKey instead of a OneToOneField.

Is this a bug, and how might it be fixed?