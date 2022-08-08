import pytest
from django.test.client import MULTIPART_CONTENT

from categories.models import Category
from categories.tests.factories.category_factory import CategoryFactory


@pytest.mark.django_db
def test_list_all_categories(logged_in_client):
    """
    Test list all products categories with empty database
    """
    response = logged_in_client.get("/v1/categories/")

    assert response.status_code == 200, response.json()
    assert len(response.json()["results"]) == 0
    assert response.json()["results"] == []


@pytest.mark.django_db
def test_list_all_product_categories(logged_in_client):
    """
    Test list all product categories
    """
    CategoryFactory()
    response = logged_in_client.get("/v1/categories/")

    response_data = response.json()["results"]

    assert response.status_code == 200, response_data
    assert len(response_data) == 1


@pytest.mark.django_db
def test_create_product_category(admin_client):
    """
    Test admin create product category
    """
    category_data = {"name": "test-category-create"}
    response = admin_client.post("/v1/categories/", category_data, format="json")
    assert response.status_code == 201 and response.json()
    assert Category.objects.count() == 1


@pytest.mark.django_db
def test_retrieve_product_category(logged_in_client):
    """
    Test retrieve specific product category
    """
    category = CategoryFactory()
    response = logged_in_client.get(f"/v1/categories/{category.id}/")

    response_data = response.json()

    assert response.status_code == 200 and response_data
    assert response_data["id"] == category.id


@pytest.mark.django_db
def test_update_product_category(admin_client):
    """
    Test update a single product category
    """
    content_type = MULTIPART_CONTENT
    category = CategoryFactory()
    data = {
        "name": "Category 1 edited",
    }
    data = admin_client._encode_json({} if not data else data, content_type)
    encoded_data = admin_client._encode_data(data, content_type)
    response = admin_client.generic(
        "PUT",
        f"/v1/categories/{category.id}/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    response_data = response.json()
    assert response.status_code == 200, response.data
    assert data["name"] == response_data["name"]


@pytest.mark.django_db
def test_patch_product_category(admin_client):
    """
    Test patch a single product property
    """
    content_type = MULTIPART_CONTENT
    category = CategoryFactory()
    data = {
        "name": "Category 1 patch edited",
    }
    data = admin_client._encode_json({} if not data else data, content_type)
    encoded_data = admin_client._encode_data(data, content_type)
    response = admin_client.generic(
        "PATCH",
        f"/v1/categories/{category.id}/",
        encoded_data,
        content_type=content_type,
        secure=False,
        enctype="multipart/form-data",
    )

    response_data = response.json()
    assert response.status_code == 200, response.data
    assert data["name"] == response_data["name"]


@pytest.mark.django_db
def test_delete_product_category(admin_client):
    """
    Test delete specific product category
    """
    category = CategoryFactory()
    response = admin_client.delete(f"/v1/categories/{category.id}/")
    assert response.status_code == 204
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_non_safe_permission_product_category_should_raise_403(logged_in_client):
    """
    Test non safe method permission access on product category
    """
    category = CategoryFactory()
    response = logged_in_client.delete(f"/v1/categories/{category.id}/")
    assert response.status_code == 403 and response.json() == {
        "detail": "You do not have permission to perform this action."
    }
