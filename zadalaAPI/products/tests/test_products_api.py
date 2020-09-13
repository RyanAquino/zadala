import pytest
from products.factories.product_factory import ProductFactory
from products.models import Product


@pytest.mark.django_db
def test_get_all_products(logged_in_client):
    """
    Test get all products
    """
    response = logged_in_client.get("/api/products")

    assert response.status_code == 200


@pytest.mark.django_db
def test_get_single_products(logged_in_client):
    """
    Test get a single products
    """
    product = ProductFactory()
    response = logged_in_client.get(f"/api/products/{product.id}")

    assert response.status_code == 200
    assert response.json()


@pytest.mark.django_db
def test_add_product(logged_in_client):
    """
    Test add new product
    """
    data = {
        "name": "product_1",
        "description": "product_1 description",
        "price": 30,
        "quantity": 5,
    }

    response = logged_in_client.post("/api/products", data, format="json")

    assert Product.objects.count() == 1
    assert response.status_code == 201, response.data


@pytest.mark.django_db
def test_delete_product(logged_in_client):
    """
    Test delete product
    """
    product = ProductFactory()
    response = logged_in_client.delete(f"/api/products/{product.id}", format="json")

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_product(logged_in_client):
    """
    Test update a single product
    """
    product = ProductFactory()
    data = {
        "name": "Product 1 edited",
        "description": "Product 1 edited description",
        "price": 0,
        "quantity": 0,
    }

    response = logged_in_client.put(
        f"/api/products/{product.id}",
        data,
        format="json",
        content_type="application/json",
    )

    response_data = response.json()
    assert response.status_code == 202, response.data
    assert data["name"] == response_data["name"]
    assert data["description"] == response_data["description"]
    assert data["price"] == response_data["price"]
    assert data["quantity"] == response_data["quantity"]
