from bson import ObjectId

from app.services.database import Database
from app.models.user import User

def check_user_exists_by_username(database: Database, username: str) -> bool:
    """
    Check if a user with the given username already exists in the database.

    Args:
        database (Database): The database service instance.
        username (str): The username to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    existing_user = database.find_one(
        collection="users",
        query={"username": username}
    )

    return existing_user is not None


def check_user_exists_by_email(database: Database, email: str) -> bool:
    """
    Check if a user with the given email already exists in the database.

    Args:
        database (Database): The database service instance.
        email (str): The email to check for existence.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    existing_user = database.find_one(
        collection="users",
        query={"email": email}
    )

    return existing_user is not None


def check_user_credentials(database: Database, username: str, password: str) -> bool:
    """
    Check if the provided username and password match a user in the database.

    Args:
        database (Database): The database service instance.
        username (str): The username to check.
        password (str): The password to check.

    Returns:
        bool: True if the credentials are valid, False otherwise.
    """
    user_data = database.find_one(
        collection="users",
        query={"username": username}
    )

    if not user_data:
        return False
    
    user = User.from_dict(user_data)
    print("CHECK_PASSWORD", password)
    return user.check_password(password)


def create_user(database: Database, user: User) -> None:
    """
    Create a new user in the database.

    Args:
        database (Database): The database service instance.
        user (User): The User instance containing user details to be created.

    Returns:
        None
    """
    database.insert_one(
        collection="users",
        query=user.to_dict()
    )


def get_user_by_id(database: Database, user_id: str | ObjectId) -> User | None:
    """
    Retrieve a user from the database by their unique identifier.

    Args:
        database (Database): The database service instance.
        user_id (str | ObjectId): The unique identifier of the user to retrieve.

    Returns:
        User | None: A User instance if found, or None if no user with the given ID exists.
    """
    
    if isinstance(user_id, str):
        try:
            user_id = ObjectId(user_id)
        except Exception as e:
            print(f"Invalid user ID format: {e}")
            return None
    user_data = database.find_one(
        collection="users",
        query={"_id": user_id}
    )

    if user_data:
        return User.from_dict(user_data)
    
    return None


def get_user_by_username(database: Database, username: str) -> User | None:
    """
    Retrieve a user from the database by their username.

    Args:
        database (Database): The database service instance.
        username (str): The username of the user to retrieve.

    Returns:
        User | None: A User instance if found, or None if no user with the given username exists.
    """
    user_data = database.find_one(
        collection="users",
        query={"username": username}
    )

    if user_data:
        return User.from_dict(user_data)
    
    return None