from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import base64
from bson.objectid import ObjectId

class User(UserMixin):
    """
    Represents a User document from the 'users' collection in database.
    """

    def __init__(
        self, username: str = None, email: str = None, password: str = None,
        image_bytes: bytes = None, attached_bots_id: [ObjectId] = [],
        collections: [ObjectId] = [], money: int = 0, _id: ObjectId = None
    ):
        self.id: str = str(_id) if _id else None  # For Flask
        self._id: ObjectId = _id
        self.username: str = username
        self.email: str = email
        self.password: str = password
        self.image_bytes: bytes = image_bytes
        self.attached_bots_id: [ObjectId] = attached_bots_id
        self.collections: [ObjectId] = collections
        self.money: int = money

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        if not self.password:
            return False

        return check_password_hash(self.password, password)

    def get_image_base64(self) -> str:
        if not self.image_bytes:
            return ""
        return base64.b64encode(self.image_bytes).decode('utf-8')

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "image": self.image_bytes,
            "attached_bots_id": self.attached_bots_id,
            "collections": self.collections,
            "money": self.money
        }

    @staticmethod
    def from_dict(data: dict) -> User:
        """Factory method to create a User object from a MongoDB document."""

        if not data:
            return None

        return User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            image_bytes=data.get('image'),
            attached_bots_id=data.get('attached_bots_id', []),
            collections=data.get('collections', []),
            money=data.get('money', 0),
            _id=data.get('_id')
        )