from uuid import uuid4

class User:
    def __init__(self, name, email, id=None):
        self.id = id if id else str(uuid4())
        self.name = name
        self.email = email

    def __repr__(self):
        return f'{self.id}, {self.name}, {self.email}'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    @staticmethod
    def from_dict(dict_value):
        return User(
            dict_value.get('name'),
            dict_value.get('email'),
            dict_value.get('id'),
        )