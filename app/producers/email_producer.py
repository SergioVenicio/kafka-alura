from models.email import Email

from .base_producer import BaseProducer


TOPIC = 'ECOMMERCE_SEND_EMAIL'


class EmailProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(EmailProducer, self).__init__(topic)

    async def send(self, email: Email):
        await self._send(email.to_dict())