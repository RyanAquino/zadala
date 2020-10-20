from orders.tests.factories.order_item_factory import OrderItemFactory
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
