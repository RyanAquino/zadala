import pytest


@pytest.mark.django_db
def test_list_all_orders(logged_in_client):
    """
    Test list all orders
    """
    response = logged_in_client.get("/api/orders")
    assert response.status_code == 200, response.data
    assert response.json() == {"total_items": 0, "total_amount": 0, "products": []}


@pytest.mark.django_db
def test_add_product_to_cart(logged_in_client):
    """
    Test adding product to a cart
    """
    response = logged_in_client.get("/api/products/")
