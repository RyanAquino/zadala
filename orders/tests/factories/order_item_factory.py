from orders.models import OrderItem
from products.tests.factories.product_factory import ProductFactory
from orders.tests.factories.order_factory import OrderFactory
from factory.django import DjangoModelFactory
import factory
import datetime


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    product = factory.SubFactory(ProductFactory)
    order = factory.SubFactory(OrderFactory)
    quantity = 35
    date_added = factory.LazyFunction(datetime.datetime.now)
