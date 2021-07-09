import json

from models.order import Order
from base_service import BaseService


TOPIC = 'ECOMMERCE_NEW_ORDER'


class FraudDetectorService(BaseService):
    def __init__(self):
        super(FraudDetectorService, self).__init__(
            TOPIC,
            FraudDetectorService.__name__
        )

    async def consume(self):
        for message in self.consumer:
            message_dict = json.loads(message.value)
            order = Order.from_dict(message_dict)
            self.consumer.commit()
            print(order)


if __name__ == '__main__':
    import asyncio

    service = FraudDetectorService()

    asyncio.run(service.consume())