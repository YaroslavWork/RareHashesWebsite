import datetime

from app.utils.notification import log

class Hash:
    ignore_vars = ['user']

    def __init__(self, word=None, isFromBeginning=None, counts=None, hashType=None, createdAt=None, user=None):
        self.word: str | None = word
        self.isFromBeginning: bool | None = isFromBeginning
        self.counts: int | None = counts
        self.hashType: str | None = hashType
        self.createdAt: datetime.datetime | None = createdAt
        self.user: str | None = user

    def is_complete(self):
        return all(getattr(self, key) is not None if key not in Hash.ignore_vars else True for key in vars(self))

    def to_dict(self):
        return {
            key: value if value is not None else "" for key, value in vars(self).items()
        }
    
    def from_dict(self, data):
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


# Testing
if __name__ == '__main__':
    d = {"word": 'abc', 'isFromBeggining': True, 'counts': 12, 'hashType': 'sha256', 'created_at': datetime.datetime.now()}
    h1 = Hash()
    h1.from_dict(d)
    print(vars(h1))
    print(h1.is_complete())