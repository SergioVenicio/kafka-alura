class Order:
    def __init__(self, id, customer, total):
        self.id = id
        self.customer = customer
        self.total = total

    def __repr__(self):
        return f'ID: {self.id}, CUSTOMER: {self.customer}, TOTAL: {self.total}'

    def to_dict(self):
        return {
            'id': self.id,
            'customer': self.customer,
            'total': self.total
        }

    @staticmethod
    def from_dict(dict_value):
        return Order(
            dict_value.get('id'),
            dict_value.get('customer'),
            dict_value.get('total'),
        )