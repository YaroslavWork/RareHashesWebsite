import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app.utils.uuid_utils import generate_uuid


def test_generate_uuid():
    # Generate a UUID and check its length
    uuid = generate_uuid()
    assert len(uuid) == 32  # UUID is 32 characters long in hex format

    # Check if the generated UUID is a valid hexadecimal string
    assert all(c in '0123456789abcdef' for c in uuid)

    # Check if the UUID is unique by generating multiple UUIDs
    uuids = {generate_uuid() for _ in range(10000)}
    assert len(uuids) == 10000  # All generated UUIDs should be unique
