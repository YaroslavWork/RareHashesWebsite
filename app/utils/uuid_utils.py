import uuid


def generate_uuid() -> str:
    """
    Generate a new UUID (Universally Unique Identifier).

    Returns:
        str: A string representation of the generated UUID.
    """
    return uuid.uuid4().hex
