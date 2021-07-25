import asyncio
import sys
import uuid

from dependency_injector.wiring import inject, Provide

from containers import Container

from repository.user_repository import UserRepository

from models.order import Order
from models.user import User
from models.report_request import ReportRequest


@inject
def order_producer(producer = Provide[Container.order_producer]):
    print('Running Order producer...')
    user_repository = UserRepository()

    while True:
        email = input("Customer email: ")
        name = input("Customer name: ")
        total = float(input("Order total: "))

        user = user_repository.get_user_by_email(email)
        _id = str(uuid.uuid4()) if not user else user.id

        order = Order(
            id=str(uuid.uuid4()),
            user=User(name, email, _id),
            total=total
        )

        asyncio.run(producer.send(order))

@inject
def fake_orders_producer(producer = Provide[Container.order_producer]):
    print('Running Fake orders producer...')

    async def create_message():
        counter = 1
        while True:
            name = str(uuid.uuid4())
            email = name + '@test.com'
            total = 100

            order = Order(
                id=str(uuid.uuid4()),
                user=User(name, email),
                total=total
            )

            await producer.send(order)
            print(f'Counter: {counter}')
            counter += 1
        
    asyncio.run(create_message())


@inject
def report_producer(producer = Provide[Container.report_producer]):
    print('Running Report producer...')
    user_repository = UserRepository()

    while True:
        email = input("Customer email: ")
        # email = 'sergiovenicio2015@gmail.com'
        user = user_repository.get_user_by_email(email)
        report_request = ReportRequest(user)

        asyncio.run(producer.send(report_request))


if __name__ ==  '__main__':
    container = Container()
    container.wire(modules=[sys.modules[__name__]])

    options = {
        1: order_producer,
        2: fake_orders_producer,
        3: report_producer
    }

    op = int(input("""\
    1 -> Order
    2 -> Fake Orders
    3 -> Report
    """))

    service = options[op]

    service()
