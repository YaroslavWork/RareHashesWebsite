import datetime

from app.utils.notification import log

class Hash:
    """
    Represents a hash object used in the application, holding metadata such as word, type, origin, timestamp, and user information.

    Attributes:
        ignore_vars (list[str]): List of attributes to ignore during completeness check.
        word (str, optional): The original word that was hashed.
        isFromBeginning (bool, optional): Whether the hash pattern appears from the beginning.
        counts (int, optional): Number of repeated signs at the start.
        hashType (str, optional): Type of hashing algorithm used.
        createdAt (datetime.datetime, optional): Timestamp when the hash was created.
        user (str, optional): Optional user who submitted the hash.
    """

    ignore_vars = ['user']

    def __init__(self, word=None, isFromBeginning=None, counts=None, hashType=None, createdAt=None, user=None):
        """
        Initialize a new Hash instance.

        Args:
            word (str, optional): The original word that was hashed.
            isFromBeginning (bool, optional): Whether the hash pattern appears from the beginning.
            counts (int, optional): Number of repeated signs at the start.
            hashType (str, optional): Type of hashing algorithm used.
            createdAt (datetime.datetime, optional): Timestamp when the hash was created.
            user (str, optional): Optional user who submitted the hash.
        """

        self.word: str | None = word
        self.isFromBeginning: bool | None = isFromBeginning
        self.counts: int | None = counts
        self.hashType: str | None = hashType
        self.createdAt: datetime.datetime | None = createdAt
        self.user: str | None = user

    def is_complete(self) -> bool:
        """
        Check whether all required fields (excluding ignored ones) are set.

        Returns:
            bool: True if all non-ignored attributes are not None, False otherwise.
        """

        return all(getattr(self, key) is not None if key not in Hash.ignore_vars else True for key in vars(self))

    def to_dict(self) -> dict:
        """
        Convert the Hash object to a dictionary representation.

        Returns:
            dict: Dictionary containing all object attributes. None values are converted to empty strings.
        """

        return {
            key: value if value is not None else "" for key, value in vars(self).items()
        }
    
    def from_dict(self, data: dict):
        """
        Load Hash attributes from a dictionary.

        Args:
            data (dict): A dictionary containing key-value pairs to set as attributes.

        Logs:
            If a key from the dictionary doesn't match an attribute, logs a warning.
        """

        for key, value in data.items():
            try:
                setattr(self, key, value)
            except AttributeError:
                log("HashModel", f"Not finding a {key}: {value}.")

    def __str__(self):
        string = "Hash:"
        for key, value in vars(self).items():
            string += f"{key}: {value}; "
        return string