from django.conf import settings
from django.contrib.postgres.indexes import GinIndex, OpClass
from django.db import models
from django.db.models.functions import Upper

from categories.models import Category


class Product(models.Model):
    supplier = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True
    )
    name = models.TextField(unique=True)
    description = models.TextField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.URLField(null=True)
    image = models.ImageField(null=True)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )

    REQUIRED_FIELDS = "__all__"

    class Meta:
        indexes = [
            GinIndex(
                OpClass(Upper("name"), name="gin_trgm_ops"),
                name="products_name_gin_index",
            )
        ]

    def __str__(self):
        return self.name
