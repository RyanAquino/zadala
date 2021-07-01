from products.models import Product
from factory.django import DjangoModelFactory
import factory


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f"Product {n}")
    description = "Product 1 description"
    price = 35
    image = None
    quantity = 3
    digital = False
