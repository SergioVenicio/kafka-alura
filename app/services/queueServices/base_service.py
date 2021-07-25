from abc import ABC, abstractmethod

import re

from kafka import KafkaConsumer
from kafka.errors import CommitFailedError


class Consumer:
    def __init__(self, consumer):
        self.consumer = consumer

    def subscribe(self, topic=None, pattern=None):
        if topic:
            self.consumer.subscribe(topic)
        else:
            self.consumer.subscribe(pattern=pattern)

    async def commit(self):
        try:
            self.consumer.commit()
        except CommitFailedError:
            return

    def __aiter__(self):
        return self

    async def __anext__(self):
        for row in self.consumer:
            return row


class BaseService(ABC):
    def __init__(self, topic, group_id):
        self.__consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            group_id=group_id,
            enable_auto_commit=False
        )
        self.consumer = Consumer(self.__consumer)
        
        if isinstance(topic, re.Pattern):
            self.consumer.subscribe(pattern=topic)
        else:
            self.consumer.subscribe(topic=[topic])

    @abstractmethod
    async def consume(self):
        pass
