from .base_producer import BaseProducer

from models.user import User

TOPIC = 'ECOMMERCE_CREATE_USER'

class UserProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(UserProducer, self).__init__(topic)

    async def send(self, user: User):
        await self._send(user.to_dict())