from app.services.database import Database
from app.models.hash import Hash

def add_hash_to_database(database: Database, hash: Hash) -> None:
    """
    Insert a hash document into the database.

    Args:
        database (Database): The database service instance.
        hash (Hash): The hash model to insert.
    """

    write_data = hash.to_dict()
    print(write_data)
    database.set_active_collection('hashes')
    database.insert_one(query=write_data)


def how_many_hashes_above(database: Database, border: int) -> int:
    """
    Count how many documents have 'counts' field greater than the given border.

    Args:
        database (Database): The database service instance.
        border (int): The border value (included that number) for counting.

    Returns:
        int: Number of documents with 'counts' greater than the border.
    """

    database.set_active_collection('hashes')
    count = database.count(query={"counts": {"$gt": border}})

    return count