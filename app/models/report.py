from models.order import Order


class Report:
    def __init__(self, user, orders):
        self.user = user
        self.orders = orders

    def __str__(self):
        return f"""
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        USER: {self.user}
        =========================
        ORDERS
        -------------------------
        {''.join(self.__order_to_str())}
        =========================
        ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        """

    def __order_to_str(self):
        for order in self.orders:
            yield f"""
            ==================================
                ORDER: {order['id']}
                TOTAL: {order['total']}
            =================================="""

    def to_dict(self):
        return {
            'user': self.user,
            'orders': self.orders
        }

    @staticmethod
    def from_dict(dict_value):
        return Report(
            dict_value.get('user'),
            dict_value.get('orders')
        )