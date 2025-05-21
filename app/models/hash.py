import datetime

class Hash:
    ignore_vars = ['user']

    def __init__(self, word=None, isFromBeggining=None, counts=None, hashType=None, created_at=None, user=None):
        self.word: str | None = word
        self.isFromBeggining: bool | None = isFromBeggining
        self.counts: int | None = counts
        self.hashType: str | None = hashType
        self.created_at: datetime.datetime | None = created_at
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
                print(f"Not finding a {key}: {value}.")


# Testing
if __name__ == '__main__':
    d = {"word": 'abc', 'isFromBeggining': True, 'counts': 12, 'hashType': 'sha256', 'created_at': datetime.datetime.now()}
    h1 = Hash()
    h1.from_dict(d)
    print(vars(h1))
    print(h1.is_complete())