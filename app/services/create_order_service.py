from repository.user_repository import UserRepository
from repository.order_repository import OrderRepository


class CreateOrderService:
    def __init__(self):
        self.repository = OrderRepository()
        self.user_repository = UserRepository()

    async def create_order(self, order):
        if self.repository.get_order_by_id(order.id):
            print(f'Order: {order.id} already exists!')
            return

        user = self.user_repository.get_user_by_email(order.user.email)
        order.user = user if user else order.user

        self.repository.create_order(order)