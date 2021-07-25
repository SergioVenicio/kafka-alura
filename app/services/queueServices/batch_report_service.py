from .base_service import BaseService

from producers.report_procuder import ReportProducer

from repository.user_repository import UserRepository

from models.report_request import ReportRequest


TOPIC = 'ECOMMERCE_REPORT_BATCH_REQUEST'


class BatchReportService(BaseService):
    def __init__(self):
        self.user_repository = UserRepository()
        self.report_producer = ReportProducer()
        super(BatchReportService, self).__init__(
            TOPIC,
            BatchReportService.__name__
        )

    async def consume(self):
        async for _ in self.consumer:
            print('Reading message...') 
            await self.consumer.commit()
            print('Message Commited!') 
            for user in self.user_repository.get_users():
                report_request = ReportRequest(user)
                await self.report_producer.send(report_request)



if __name__ == '__main__':
    import asyncio

    service = BatchReportService()
    asyncio.run(service.consume())