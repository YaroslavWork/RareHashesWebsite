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


def get_hashes_in_ranges(database: Database, start_index: int, end_index: int, sort_data: list=[]) -> list[Hash]:
    """
    Retrieve a list of Hash objects from the database within a specified range and sorted by given criteria.

    Args:
        database (Database): The database service instance.
        start_index (int): The number of documents to skip (offset).
        end_index (int): The maximum number of documents to return (limit).
        sort_data (list, optional): Sorting criteria as a list of tuples, e.g.  [(counts, -1), (createdAt, 1)]. Defaults to [].

    Returns:
        list[Hash]: A list of Hash instances retrieved from the database.
    """

    database.set_active_collection('hashes')
    results: dict = database.find(
            query={},
            sort=sort_data,
            skip=start_index,
            limit=end_index
        )
    
    hashes: list[Hash] = []
    for result in results:
        hash = Hash()
        hash.from_dict(result)
        hashes.append(hash)
    
    return hashes


def is_hash_in_database(database: Database, word: str) -> bool:
    """
    Search in the database if this hash is already exists.

    Args:
        database (Database): The database service instance.
        word (str): The hash word

    Returns:
        bool: Return True if hash is already in the database.
    """

    database.set_active_collection('hashes')
    result = database.find_one(query={"word": word})
    if not result:
        return False
    return True