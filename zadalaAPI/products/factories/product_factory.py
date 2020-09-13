from products.models import Product
from factory.django import DjangoModelFactory


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = "Product 1"
    description = "Product 1 description"
    price = 35
    image = None
    quantity = 3
