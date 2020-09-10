"""
Pytest global shared fixtures
"""
import pytest


# @pytest.fixture(scope='session')
# def client():
#     client = app.test_client()
#     return client
#
#
# @pytest.fixture
# def delete_after_post(request, url, client):
#     def cleanup():
#         urlf = f"{url}/{request.node.id}"
#         client.delete(urlf)
#
#     request.addfinalizer(cleanup)
#
#
# @pytest.fixture
# def create_after_deleted(request, url, client):
#     def cleanup():
#         data = {"id": request.node.id, "name": "this is new model!"}
#         client.post(url, json=data)
#
#     request.addfinalizer(cleanup)