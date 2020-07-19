from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=191)
    description = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    picture = models.CharField(max_length=255)
    quantity = models.IntegerField(default=0)

    REQUIRED_FIELDS = '__all__'

    def __str__(self):
        return self.name
