from datetime import datetime
from unittest.mock import patch

import pytest

from orders.models import Order, OrderItem
from orders.tests.factories.order_factory import OrderFactory
from orders.tests.factories.order_item_factory import OrderItemFactory
from products.tests.factories.product_factory import ProductFactory


@pytest.mark.django_db
def test_list_all_orders_with_empty_database(logged_in_client):
    """
    Test list all orders with empty database
    """
    response = logged_in_client.get("/v1/orders/")
    assert response.status_code == 200, response.data
    assert response.json() == {"total_items": 0, "total_amount": 0, "products": []}


@pytest.mark.django_db
def test_list_all_orders_sorted_by_date_added(logged_in_client, logged_in_user):
    customer_order = OrderFactory(customer=logged_in_user)
    date_format = "%Y-%m-%d"
    first_order_date = "2021-11-20"
    second_order_date = "2021-11-25"
    third_order_date = "2021-11-26"

    OrderItemFactory(
        order=customer_order,
        date_added=datetime.strptime(first_order_date, date_format),
    )
    OrderItemFactory(
        order=customer_order,
        date_added=datetime.strptime(second_order_date, date_format),
    )
    OrderItemFactory(
        order=customer_order,
        date_added=datetime.strptime(third_order_date, date_format),
    )

    response = logged_in_client.get("/v1/orders/")
    response_data = response.json()
    sorted_dates = [
        order_item["date_added"] for order_item in response_data["products"]
    ]
    assert sorted_dates == [
        "2021-11-26T00:00:00Z",
        "2021-11-25T00:00:00Z",
        "2021-11-20T00:00:00Z",
    ]


@pytest.mark.django_db
def test_list_all_orders(logged_in_client, logged_in_user):
    """
    Test list all orders
    """
    customer_order = OrderFactory(id=1, customer=logged_in_user)
    product = ProductFactory(name="Product 0")
    order_item = OrderItemFactory(id=1, order=customer_order, product=product)

    response = logged_in_client.get("/v1/orders/")
    response_data = response.json()

    assert response.status_code == 200, response.data
    assert response_data["total_items"] == 35
    assert response_data["total_amount"] == 1225.0

    order_details = response_data["products"][0]
    product_details = order_details["product"]

    assert str(customer_order) == "1"
    assert str(order_item) == "1"
    assert product_details["name"] == "Product 0"
    assert product_details["description"] == "Product 1 description"
    assert product_details["price"] == "35.00"
    assert product_details["quantity"] == 3
    assert order_details["order"] == 1
    assert order_details["quantity"] == 35
    assert order_details["total"] == 1225.0


@pytest.mark.django_db
def test_update_cart_product_id_not_existing(logged_in_client, logged_in_user):
    """
    Test update cart with product id not existing
    """
    OrderItemFactory()
    non_existing_product_id = 0
    data = {"productId": non_existing_product_id, "action": "add"}

    response = logged_in_client.post(f"/v1/orders/update-cart/", data=data)
    response_data = response.json()

    assert response.status_code == 404
    assert response_data == {"detail": "Not found."}


@pytest.mark.django_db
def test_update_cart_exceeding_max_product_stock_quantity(
    logged_in_client, logged_in_user
):
    """
    Test add products to a cart with exceeding product stock quantity
    """
    product_quantity = 5
    order = OrderFactory(customer=logged_in_user)
    product = ProductFactory(quantity=product_quantity)
    OrderItemFactory(order=order, product=product, quantity=product_quantity)
    product_id = product.id
    data = {"productId": product_id, "action": "add"}

    response = logged_in_client.post(f"/v1/orders/update-cart/", data=data)
    response_data = response.json()

    assert response.status_code == 422
    assert response_data == {"detail": "Order Item quantity exceeds available stock"}


@pytest.mark.django_db
def test_update_cart(logged_in_client):
    """
    Test updating products of a cart
    """
    order_item = OrderItemFactory()
    product_id = order_item.product.id
    data = {"productId": product_id, "action": "add"}

    response = logged_in_client.post(f"/v1/orders/update-cart/", data=data)
    response_data = response.json()
    order_items = response_data["products"]

    assert response.status_code == 201
    assert response_data["total_items"] == 1
    assert response_data["total_amount"] == 35
    assert len(order_items) == 1

    data = {"productId": product_id, "action": "remove"}

    response = logged_in_client.post(f"/v1/orders/update-cart/", data=data)
    response_data = response.json()
    order_items = response_data["products"]

    assert response.status_code == 201
    assert response_data["total_items"] == 0
    assert response_data["total_amount"] == 0
    assert len(order_items) == 0


@pytest.mark.django_db
@patch("django_rq.enqueue", lambda *args: args)
def test_process_order(logged_in_client, logged_in_user):
    """
    Test process order
    """
    order = OrderFactory(customer=logged_in_user)
    OrderItemFactory(order=order)

    data = {
        "address": "My Address",
        "city": "Baguio",
        "state": "Benguet",
        "zipcode": "2600",
    }
    response = logged_in_client.post(f"/v1/orders/process-order/", data=data)

    assert response.status_code == 201


@pytest.mark.django_db
def test_process_order_not_found(logged_in_client, logged_in_user):
    """
    Test process invalid order
    """
    data = {
        "address": "My Address",
        "city": "Baguio",
        "state": "Benguet",
        "zipcode": "2600",
    }
    response = logged_in_client.post(f"/v1/orders/process-order/", data=data)

    assert response.status_code == 400
    assert response.json() == "Order not found"


@pytest.mark.django_db
def test_delete_single_order_item_should_delete_main_order(logged_in_user):
    OrderItemFactory()
    OrderItem.objects.first().delete()
    assert OrderItem.objects.count() == 0 and Order.objects.count() == 0


@pytest.mark.django_db
def test_multiple_order_items_should_not_delete_main_order(logged_in_user):
    OrderItemFactory.create_batch(5)
    OrderItem.objects.first().delete()
    assert OrderItem.objects.count() == 4 and Order.objects.count() == 4


@pytest.mark.django_db
def test_update_cart_response_sorted_by_date_added(logged_in_client, logged_in_user):
    order = OrderFactory(customer=logged_in_user)
    date_format = "%Y-%m-%d"
    first_order_date = "2021-11-20"
    second_order_date = "2021-11-25"
    third_order_date = "2021-11-26"

    OrderItemFactory(
        date_added=datetime.strptime(second_order_date, date_format),
        order=order,
        quantity=1,
    )
    OrderItemFactory(
        date_added=datetime.strptime(third_order_date, date_format),
        order=order,
        quantity=1,
    )
    first_order = OrderItemFactory(
        date_added=datetime.strptime(first_order_date, date_format),
        order=order,
        quantity=1,
    )
    product_id = first_order.product.id

    data = {"productId": product_id, "action": "add"}

    response = logged_in_client.post(f"/v1/orders/update-cart/", data=data)
    response_data = response.json()
    sorted_dates = [
        order_item["date_added"] for order_item in response_data["products"]
    ]

    assert sorted_dates == [
        "2021-11-26T00:00:00Z",
        "2021-11-25T00:00:00Z",
        "2021-11-20T00:00:00Z",
    ]
