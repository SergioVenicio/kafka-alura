from .base_producer import BaseProducer
from .email_producer import EmailProducer

from models.order import Order
from models.email import Email

TOPIC = 'ECOMMERCE_NEW_ORDER'


class OrderProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(OrderProducer, self).__init__(topic)
        self.email_producer = EmailProducer()

    async def send(self, order: Order):
        await self._send(order.to_dict())