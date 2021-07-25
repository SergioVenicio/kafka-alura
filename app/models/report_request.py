from repository.order_repository import OrderRepository

class ReportRequest:
    def __init__(self, user):
        self.order_repository = OrderRepository()
        self.user = user
        self.orders = self.__load_orders(user)

    def __load_orders(self, user):
        orders = self.order_repository.get_orders_by_user_id(user.id)
        return orders

    def to_dict(self):
        return {
            'user': self.user.email,
            'orders': [order.to_dict() for order in self.orders]
        }

    @staticmethod
    def from_dict(dict_value):
        return ReportRequest(
            dict_value.get('user')
        )