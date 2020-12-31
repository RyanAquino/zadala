from orders.tests.factories.order_item_factory import OrderItemFactory
from orders.tests.factories.order_factory import OrderFactory
import pytest


@pytest.mark.django_db
def test_list_all_orders_with_empty_database(logged_in_client):
    """
    Test list all orders with empty database
    """
    response = logged_in_client.get("/v1/orders/")
    assert response.status_code == 200, response.data
    assert response.json() == {"total_items": 0, "total_amount": 0, "products": []}


@pytest.mark.django_db
def test_list_all_orders(logged_in_client, logged_in_user):
    """
    Test list all orders
    """
    customer_order = OrderFactory(customer=logged_in_user)
    order_item = OrderItemFactory(order=customer_order)

    response = logged_in_client.get("/v1/orders/")
    response_data = response.json()

    assert response.status_code == 200, response.data
    assert response_data["total_items"] == 35
    assert response_data["total_amount"] == 1225.0

    order_details = response_data["products"][0]
    product_details = order_details["product"]

    assert str(customer_order) == "2"
    assert str(order_item) == "1"
    assert product_details["name"] == "Product 1"
    assert product_details["description"] == "Product 1 description"
    assert product_details["price"] == 35.0
    assert product_details["quantity"] == 3
    assert order_details["order"] == 2
    assert order_details["quantity"] == 35
    assert order_details["total"] == 1225.0


@pytest.mark.django_db
def test_update_cart(logged_in_client):
    """
    Test updating products of a cart
    """
    order_item = OrderItemFactory()
    product_id = order_item.product.id
    order_id = order_item.order.id
    data = {"productId": product_id, "action": "add"}

    response = logged_in_client.post(f"/v1/orders/{order_id}/update-cart/", data=data)

    assert response.status_code == 200

    data = {"productId": product_id, "action": "remove"}

    response = logged_in_client.post(f"/v1/orders/{order_id}/update-cart/", data=data)

    assert response.status_code == 200


@pytest.mark.django_db
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
