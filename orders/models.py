from django.utils import timezone
from django.db import models
from authentication.models import User
from products.models import Product
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        order_items = self.orderitem_set.all()

        for i in order_items:
            if not i.product.digital:
                shipping = True

        return shipping

    @property
    def order_items(self):
        return self.orderitem_set.all()

    @property
    def get_cart_total(self):
        items = self.order_items
        total = sum([item.total for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.order_items
        total = sum([item.quantity for item in items])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True)
    date_added = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return str(self.id)

    @property
    def total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):  # pragma: no cover
        return str(self.address)


@receiver(post_delete, sender="orders.OrderItem")
def delete_order(sender, instance: OrderItem, **kwargs):
    order_id = instance.order_id
    order_items = OrderItem.objects.filter(order_id=instance.order_id).count()

    if order_items == 0:
        Order.objects.get(pk=order_id).delete()
