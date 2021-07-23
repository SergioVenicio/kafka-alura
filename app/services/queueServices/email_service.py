import json

from .base_service import BaseService
from models.email import Email


TOPIC = 'ECOMMERCE_SEND_EMAIL'

class SendEmailService(BaseService):
    def __init__(self):
        super(SendEmailService, self).__init__(
            TOPIC,
            SendEmailService.__name__
        )

    async def consume(self):
        async for message in self.consumer:
            try:
                message_dict = json.loads(message.value)
                email = Email.from_dict(message_dict)
                print(email)
            except Exception:
                print(message.value.decode('utf8'))
            finally:
                await self.consumer.commit()
