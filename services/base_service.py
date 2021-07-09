import re
import json
from abc import ABC, abstractmethod

from kafka import KafkaConsumer


class BaseService(ABC):
    def __init__(self, topic, group_id):
        self.consumer = KafkaConsumer(
            bootstrap_servers='localhost:9092',
            group_id=group_id,
            enable_auto_commit=False
        )
        
        if isinstance(topic, re.Pattern):
            self.consumer.subscribe(pattern=topic)
        else:
            self.consumer.subscribe([topic])

    @abstractmethod
    async def consume(self):
        pass
