import json

from models.order import Order
from models.email import Email

from producers.email_producer import EmailProducer
from producers.user_producer import UserProducer

from services.create_order_service import CreateOrderService

from .base_service import BaseService

TOPIC = 'ECOMMERCE_NEW_ORDER'


class FraudDetectorService(BaseService):
    def __init__(self):
        super(FraudDetectorService, self).__init__(
            TOPIC,
            FraudDetectorService.__name__
        )

        self.email_producer = EmailProducer()
        self.user_producer = UserProducer()
        self.create_service = CreateOrderService()

    async def consume(self):
        async for message in self.consumer:
            message_dict = json.loads(message.value)
            order = Order.from_dict(message_dict)

            await self.user_producer.send(order.user)
            await self.create_service.create_order(order)

            if order.total >= 4500:
                email = Email(
                    email_from='suport@kafka.com',
                    email_to=order.user.email,
                    subject=f'Order {order.id}',
                    body=f'Hello {order.user.name} Purshe {order.id} is a fraud!!!'
                )
            else:
                email = Email(
                    email_from='suport@kafka.com',
                    email_to=order.user.email,
                    subject=f'Thank you {order.user.name}',
                    body=f'Purshe {order.id} is being processed'
                )

            await self.consumer.commit()
            await self.email_producer.send(email)
