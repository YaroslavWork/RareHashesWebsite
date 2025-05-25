import pytest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app

@pytest.fixture
def start():
    app = create_app()
    with app.test_client() as client:
        yield client, app


def test_write(start):
    client, app = start

    response = client.get('/write')
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("text/html")

    response = client.post('/write', json={})
    assert response.status_code == 400
    assert response.get_json() == {"msg": "You need to provide a 'word'."}

    response = client.post('/write', json={"foo": "foo"})
    assert response.status_code == 400
    assert response.get_json() == {"msg": "You need to provide a 'word'."}

    response = client.post('/write', json={"word": "tooLong"*100})
    assert response.status_code == 400
    pattern = r"You reach the max length of the word\. Max length is \d+ \(Your: (\d+)\)\."
    message = response.get_json().get("msg")
    assert re.fullmatch(pattern, message)

    response = client.post('/write', json={"word": "good"})
    assert response.status_code == 400
    assert response.get_json() == {"msg": "You need to provide a 'hashType' (Current support: sha256)."}

    response = client.post('/write', json={"word": "good", "user": "tooLong"*10})
    assert response.status_code == 400
    pattern = r"You reach the max length of the user\. Max length is \d+ \(Your: (\d+)\)\."
    message = response.get_json().get("msg")
    assert re.fullmatch(pattern, message)

    response = client.post('/write', json={"word": "hello1234qweasd", "user": "test", "hashType": "sha256"})
    assert response.status_code == 400
    pattern = r"Your hash has lower that \d+ repeated signs \(4\)\. "
    message = response.get_json().get("msg")
    assert response.get_json().get("errno") == 2
    assert re.fullmatch(pattern, message)

    response = client.post('/write', json={"word": "?F3$tjUo\"31P2JH$X(3O}.H&-HR0jq[3", "user": "test unit", "hashType": "sha256"})
    assert response.status_code == 201
    assert response.get_json() == {"errno": 0, "msg": "Hash is successfully added."}

    response = client.post('/write', json={"word": "?F3$tjUo\"31P2JH$X(3O}.H&-HR0jq[3", "user": "test unit", "hashType": "sha256"})
    assert response.status_code == 400
    assert response.get_json() == {"errno": 1, "msg": "This hash is already in database."}

    app.config['DATABASE'].set_active_collection('hashes')
    app.config['DATABASE'].delete_one({'word': '?F3$tjUo\"31P2JH$X(3O}.H&-HR0jq[3'})  # Delete hash to check next time