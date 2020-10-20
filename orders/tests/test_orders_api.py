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
    OrderItemFactory(order=customer_order)

    response = logged_in_client.get("/v1/orders/")
    response_data = response.json()

    assert response.status_code == 200, response.data
    assert response_data["total_items"] == 35
    assert response_data["total_amount"] == 1225.0
    assert response_data["products"] == [
        {
            "product": {
                "id": 1,
                "name": "Product 1",
                "description": "Product 1 description",
                "digital": False,
                "price": 35.0,
                "image": None,
                "quantity": 3,
                "created_at": "2020-10-20T12:30:57.951759Z",
                "supplier": None,
            },
            "order": 1,
            "quantity": 35,
            "date_added": "2020-10-20T12:30:57.955888Z",
            "total": 1225.0,
        }
    ]


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
