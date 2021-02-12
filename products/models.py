from django.db import models
from django.conf import settings


class Product(models.Model):
    supplier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    name = models.TextField(unique=True)
    description = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    price = models.FloatField(default=0)
    image_url = models.URLField(null=True)
    image = models.ImageField(null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = "__all__"

    def __str__(self):
        return self.name
