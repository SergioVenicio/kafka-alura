from models.report import Report

from .base_producer import BaseProducer

TOPIC = 'ECOMMERCE_REPORT_REQUEST'


class ReportProducer(BaseProducer):
    def __init__(self, topic=TOPIC):
        super(ReportProducer, self).__init__(topic, 0)

    async def send(self, report: Report):
        await self._send(report.to_dict())