import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app

@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client


def test_default(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")

    response = client.post('/', json={'foo': 'foo'})
    assert response.status_code == 405