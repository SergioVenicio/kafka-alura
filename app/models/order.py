from models.user import User


class Order:
    def __init__(self, id, user, total):
        self.id = id
        self.user = user
        self.total = total

    def __repr__(self):
        return f'ID: {self.id}, CUSTOMER: {self.user}, TOTAL: {self.total}'

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.to_dict(),
            'total': self.total
        }

    @staticmethod
    def from_dict(dict_value):
        return Order(
            dict_value.get('id'),
            User(
                dict_value.get('user')['name'],
                dict_value.get('user')['email'],
                dict_value.get('user')['id']
            ),
            dict_value.get('total'),
        )