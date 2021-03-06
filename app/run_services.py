import asyncio
import sys

from dependency_injector.wiring import inject, Provide

from containers import Container
from services.queueServices.logger_service import LoggerService


@inject
def email_service(service = Provide[Container.send_email_service]):
    print('Running Email service...')
    asyncio.run(service.consume())


@inject
def logger_service(service: LoggerService = Provide[Container.logger_service]):
    print('Running Logger service...')
    asyncio.run(service.consume())


@inject
def fraud_service(service = Provide[Container.fraud_detector_service]):
    print('Running Fraud service...')
    asyncio.run(service.consume())


@inject
def user_service(service = Provide[Container.user_service]):
    print('Running User service...')
    asyncio.run(service.consume())


@inject
def batch_report_service(service = Provide[Container.batch_report_service]):
    print('Running BatchReport service...')
    asyncio.run(service.consume())


@inject
def report_service(service = Provide[Container.report_service]):
    print('Running Report service...')
    asyncio.run(service.consume())



if __name__ ==  '__main__':
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    options = {
        1: logger_service,
        2: email_service,
        3: fraud_service,
        4: user_service,
        5: batch_report_service,
        6: report_service
    }

    op = int(input("""\
    1 -> Logger
    2 -> Email
    3 -> Fraud
    4 -> User
    5 -> Batch Report
    6 -> Report
    """))

    service = options[op]

    service()