import pytest
import sys
import os
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.models.hash import Hash


def test_hash():
    hash = Hash()
    data = {'word': 'test', 'isFromBeginning': True, 'counts': 12, 'hashType': 'sha256', 'createdAt': '2025-05-25 11:56:42.932000'}

    assert hash.is_complete == False

    hash.from_dict(data)
    assert hash.word == data['word']
    assert hash.isFromBeginning == data['isFromBeginning']
    assert hash.counts == data['counts']
    assert hash.hashType == data['hashType']
    assert hash.createdAt == data['createdAt']

    assert type(hash.word) == str
    assert type(hash.isFromBeginning) == bool
    assert type(hash.counts) == int
    assert type(hash.hashType) == str
    assert type(hash.createdAt) == datetime.datetime
    assert type(hash.user) == None

    assert hash.is_complete == True

    hash = Hash(
        word='Hello',
        isFromBeginning=True,
        counts=12,
        hashType='sha256',
        createdAt=datetime.datetime(2025, 4, 12, 12, 34, 3, 123),
        user=None
    )

    assert hash.is_complete == True

    data = hash.to_dict()

    assert data.get('word') == 'Hello'
    assert data.get('isFromBeginning') == True
    assert data.get('counts') == 12
    assert data.get('hashType') == 'sha256'
    assert data.get('createdAt') == '(2025, 4, 12, 12, 34, 3, 123)'
    assert data.get('user', 'foo') == 'foo'