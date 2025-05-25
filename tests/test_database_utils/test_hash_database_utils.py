import pytest
import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app
from app.database_utils.hash_database_utils import *
from app.models.hash import Hash

@pytest.fixture
def start():
    app = create_app()
    yield app


def test_add_hash_to_database(start):
    app = start
    database = app.config['DATABASE']
    database.set_active_collection('hashes')

    test_hash = Hash(word='testWord', isFromBeginning=True, counts=1, hashType='sha256', createdAt=0, user='unitTest')
    add_hash_to_database(database, test_hash)

    result = database.find_one(query={'word': 'testWord'})
    assert result is not None

    assert how_many_hashes_above(database, 100) == 0  # I dream that this unit test will fail XD
    assert how_many_hashes_above(database, 0) > 0

    results = get_hashes_in_ranges(database, 0, 5)
    assert len(results) == 5
    for result in results:
        assert type(result) == Hash

    assert is_hash_in_database(database, 'testWord') == True
    assert is_hash_in_database(database, 'hello') == False

    assert count_all_hashes(database) > 0

    database.delete({'word': 'testWord'})