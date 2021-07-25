import os
import json

from datetime import datetime

from models.report import Report

from .base_service import BaseService


TOPIC = 'ECOMMERCE_REPORT_REQUEST'


class ReportService(BaseService):
    def __init__(self):
        super(ReportService, self).__init__(
            TOPIC,
            ReportService.__name__
        )

    async def consume(self):
        def create_reports_file_location(report):
            _date = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")
            today = datetime.now().strftime("%Y%m%d")
            return f'reports/{today}/{report.user}/{_date}_{report.user}_report.txt'

        async for message in self.consumer:
            message_dict = json.loads(message.value)
            report = Report.from_dict(message_dict)
            file_name = create_reports_file_location(report)

            print(f'Writing report: {file_name}')

            file_dir = os.path.dirname(file_name)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

            with open(file_name, 'w') as _file:
                _file.write(str(report))
            await self.consumer.commit()



if __name__ == '__main__':
    import asyncio

    service = ReportService()
    asyncio.run(service.consume())