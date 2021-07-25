from .base_producer import BaseProducer

TOPIC = 'ECOMMERCE_REPORT_BATCH_REQUEST'


class BatchReportProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(BatchReportProducer, self).__init__(topic, 0)

    async def send(self, message):
        await self._send(message)