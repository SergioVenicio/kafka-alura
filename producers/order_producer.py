from models.order import Order
from models.email import Email

from base_producer import BaseProducer
from email_producer import EmailProducer

TOPIC = 'ECOMMERCE_NEW_ORDER'


class OrderProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(OrderProducer, self).__init__(topic)
        self.email_producer = EmailProducer()

    async def send(self, order: Order):
        email = Email(
            email_from='suport@kafka.com',
            email_to=order.customer,
            subject=f'Thank you {order.customer}',
            body=f'Purshe {order.id} is being processed'
        )
        await self._send(order.to_dict())
        await self.email_producer.send(email)