import pytest
from django.contrib.auth.models import Group
from django.test.client import MULTIPART_CONTENT, Client

from authentication.tests.factories.user_factory import UserFactory
from products.models import Product
from products.tests.factories.product_factory import ProductFactory


@pytest.mark.django_db
def test_list_all_products_with_empty_db(logged_in_client):
    """
    Test list all products with empty database
    """
    response = logged_in_client.get("/v1/products/")

    assert response.status_code == 200, response.json()
    assert len(response.json()["results"]) == 0
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_list_all_products(logged_in_client):
    """
    Test list all products
    """
    ProductFactory()
    response = logged_in_client.get("/v1/products/")

    response_data = response.json()["results"]

    assert response.status_code == 200, response_data
    assert len(response_data) == 1


@pytest.mark.django_db
def test_retrieve_product(logged_in_client):
    """
    Test retrieve a single product
    """
    product = ProductFactory(name="Product Name")
    response = logged_in_client.get(f"/v1/products/{product.id}/")

    response_data = response.json()

    assert str(product) == "Product Name"
    assert response.status_code == 200
    assert response_data["name"] == "Product Name"
    assert response_data["description"] == "Product 1 description"
    assert response_data["price"] == "35.00"
    assert response_data["quantity"] == 3


@pytest.mark.django_db
def test_create_product(logged_in_client):
    """
    Test create a new product
    """
    data = {
        "name": "product_1",
        "description": "product_1 description",
        "price": 30,
        "quantity": 5,
    }

    response = logged_in_client.post("/v1/products/", data, format="json")

    assert Product.objects.count() == 1
    assert response.status_code == 201, response.data


@pytest.mark.django_db
def test_delete_product(logged_in_client, logged_in_user):
    """
    Test delete a product
    """
    product = ProductFactory(supplier=logged_in_user)
    response = logged_in_client.delete(f"/v1/products/{product.id}/", format="json")

    assert response.status_code == 204


@pytest.mark.django_db
def test_update_product(logged_in_client, logged_in_user):
    """
    Test update a single product
    """
    content_type = MULTIPART_CONTENT
    product = ProductFactory(supplier=logged_in_user)
    data = {
        "name": "Product 1 edited",
        "description": "Product 1 edited description",
        "price": "1.00",
        "quantity": 0,
        "image": {},
    }

    data = logged_in_client._encode_json({} if not data else data, content_type)
    encoded_data = logged_in_client._encode_data(data, content_type)
    response = logged_in_client.generic(
        "PUT",
        f"/v1/products/{product.id}/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    response_data = response.json()
    assert response.status_code == 200, response.data
    assert data["name"] == response_data["name"]
    assert data["description"] == response_data["description"]
    assert data["price"] == response_data["price"]
    assert data["quantity"] == response_data["quantity"]


@pytest.mark.django_db
def test_patch_product_with_different_supplier(logged_in_user):
    """
    Test update a product created by different supplier
    """
    other_user = UserFactory.create(groups=Group.objects.all())
    other_client = Client(HTTP_AUTHORIZATION=f"Bearer {other_user.tokens().token}")
    content_type = MULTIPART_CONTENT
    product = ProductFactory(supplier=logged_in_user)
    data = {
        "name": "Product 1 edited",
    }
    data = other_client._encode_json({} if not data else data, content_type)
    encoded_data = other_client._encode_data(data, content_type)
    response = other_client.generic(
        "PATCH",
        f"/v1/products/{product.id}/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    assert response.status_code == 403
    assert response.json() == {
        "detail": "You do not have permission to perform this action."
    }


@pytest.mark.django_db
def test_patch_product(logged_in_client, logged_in_user):
    """
    Test patch a single product property
    """
    content_type = MULTIPART_CONTENT
    product = ProductFactory(supplier=logged_in_user)
    data = {
        "name": "Product 1 edited",
    }

    data = logged_in_client._encode_json({} if not data else data, content_type)
    encoded_data = logged_in_client._encode_data(data, content_type)
    response = logged_in_client.generic(
        "PATCH",
        f"/v1/products/{product.id}/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    response_data = response.json()
    assert response.status_code == 200, response.data
    assert data["name"] == response_data["name"]


@pytest.mark.django_db
def test_search_product_name_filter(logged_in_client):
    """
    Test filter products by name
    """
    ProductFactory(name="Sample Product Name")
    ProductFactory.create_batch(5)
    search_params = {"search": "Sample Product Name"}
    response = logged_in_client.get("/v1/products/", search_params)
    data = response.json()

    assert response.status_code == 200
    assert Product.objects.count() == 6
    assert data["count"] == 1 and len(data["results"]) == 1
    assert data["results"][0]["name"] == "Sample Product Name"
