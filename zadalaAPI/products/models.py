from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=191)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    picture = models.CharField(max_length=255)
    quantity = models.IntegerField()
