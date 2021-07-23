import json

from .base_service import BaseService
from models.user import User
from repository.user_repository import UserRepository


TOPIC = 'ECOMMERCE_CREATE_USER'


class UserService(BaseService):
    def __init__(self):
        super(UserService, self).__init__(
            TOPIC,
            UserService.__name__
        )

        self.repository = UserRepository()

    async def consume(self):
        async for message in self.consumer:
            try:
                message_dict = json.loads(message.value)
                user = User.from_dict(message_dict)
                if not self.repository.get_user_by_email(user.email):
                    await self.repository.create_user(user)
            except Exception:
                print(message.value.decode('utf8'))
            finally:
                await self.consumer.commit()


if __name__ == '__main__':
    import asyncio

    service = UserService()
    asyncio.run(service.consume())