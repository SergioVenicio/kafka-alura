import re
from datetime import datetime

from .base_service import BaseService


TOPIC = re.compile('ECOMMERCE.*')


class LoggerService(BaseService):
    def __init__(self):
        super(LoggerService, self).__init__(
            TOPIC,
            LoggerService.__name__
        )

    async def consume(self):
        async for message in self.consumer:
            msg_value = message.value.decode('utf8')
            msg_date = datetime.utcfromtimestamp(
                message.timestamp // 1000
            ).strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{msg_date}][{message.topic}] {msg_value}')



if __name__ == '__main__':
    import asyncio

    service = LoggerService()
    asyncio.run(service.consume())