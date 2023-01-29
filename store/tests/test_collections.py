from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient
import pytest


@pytest.mark.django_db
class TestCreateCollection:
    def test_if_user_is_anonymous_returns_401(self):
        client = APIClient()
        response = client.post(
            "/store/collections/",
            {
                "title": "Collection title",
            },
        )
        assert response.status_code == HTTP_401_UNAUTHORIZED
