import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app

@pytest.fixture
def client():
    with create_app().test_client() as client:
        yield client


def test_view(client):
    response = client.get('/view')
    assert response.status_code == 302

    response = client.post('/view', json={'foo': 'foo'})
    assert response.status_code == 405


def test_view_with_params(client):
    response = client.get('/view/1123')
    assert response.status_code == 200

    response = client.get('/view/200')
    assert response.status_code == 200

    response = client.get('/view/-1')
    assert response.status_code == 404

    response = client.get('/view/1?createdAt=-1')
    assert response.status_code == 200

    response = client.get('/view/1?createdAt=0')
    assert response.status_code == 200

    response = client.get('/view/1?createdAt=foo')
    assert response.status_code == 200  # Just ignore bad requests

    response = client.get('/view/1?createdAt=-1&counts=-1')
    assert response.status_code == 200

    response = client.post('/view', json={'foo': 'foo'})
    assert response.status_code == 405