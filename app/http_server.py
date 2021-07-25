import asyncio
import json
import uuid
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

from producers.order_producer import OrderProducer
from producers.batch_report_producer import BatchReportProducer

from repository.user_repository import UserRepository

from models.user import User
from models.order import Order


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.timeout = 500
        self.routes = {
            '/': self.main,
            '/orders': self.orders_route,
            '/reports': self.generate_reports
        }
        self.order_producer = OrderProducer()
        self.report_producer = BatchReportProducer()
        self.user_repository = UserRepository()
        super().__init__(request, client_address, server)

    def main(self):
        return {'status': 200, 'message': 'server online'}

    def orders_route(self):
        try:
            event_loop = asyncio.get_event_loop()
        except RuntimeError:
            event_loop = asyncio.new_event_loop()

        params = self.get_url_params()

        if not params:
            return

        user = self.user_repository.get_user_by_email(params['email'])
        if not user:
            user = User(
                params['name'],
                params['email'],
                str(uuid.uuid4())
            )

        order = Order(
            str(uuid.uuid4()),
            user,
            params['total'],
        )
        
        event_loop.run_until_complete(self.order_producer.send(order))

        return {'status': 201, 'message': 'Order created'}

    def generate_reports(self):
        asyncio.run(self.report_producer.send('SEND_REPORT_TO_ALL_USERS'))
        return {'status': 201, 'message': 'Reports requests created'}


    def _write_response(self, response):
        self.send_response(response['status'])
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': response['message']}).encode('utf8'))

    def get_url_params(self):
        query_params = urlparse(self.path).query
        return self.validate_params(parse_qs(query_params))

    def validate_params(self, params):
        try:
            name = params.get('name', [])[0]
        except IndexError:
            name = None

        try:
            email = params.get('email', [])[0]
        except IndexError:
            email = None

        try:
            total = params.get('total', [])[0]
        except IndexError:
            total = None

        if not name or not email or not total:
            self._write_response({
                'status': 400,
                'message': 'Invalid Parameters'
            })
            return False

        return {'name': name, 'email': email, 'total': float(total)}

    def do_GET(self):
        path_without_args = self.path.split('?')[0]
        response_method = self.routes.get(path_without_args)
        if response_method is None:
            return self._write_response({
                'status': 404, 'message': 'page not found'
            })
        return self._write_response(response_method())
        


def run():
    server = HTTPServer(
        ('', 8080),
        HttpHandler
    )

    server.serve_forever()

if __name__ == '__main__':
    run()