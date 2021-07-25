from abc import ABC, abstractmethod
import uuid
import json

from kafka import KafkaProducer


class BaseProducer(ABC):
    def __init__(self, topic='', acks='all'):
        self.producer = KafkaProducer(
            bootstrap_servers='localhost:9092',
            value_serializer=BaseProducer.value_serializer,
            key_serializer=BaseProducer.key_serializer,
            acks=acks
        )
        self.__topic = topic

    @staticmethod
    def value_serializer(message):
        return json.dumps(message).encode('ascii')

    @staticmethod
    def key_serializer(key):
        try:
            return key.encode('ascii')
        except Exception:
            return key

    async def _send(self, record: str):
        self.producer.send(self.__topic, record, key=str(uuid.uuid4()))
        print(f'Message sended to {self.__topic}...')

    @abstractmethod
    async def send(self, record):
        pass