from django.db import models
from django.conf import settings


class Product(models.Model):
    supplier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    name = models.CharField(max_length=191, unique=True)
    description = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    image = models.ImageField(null=True)
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = "__all__"

    def __str__(self):
        return self.name
