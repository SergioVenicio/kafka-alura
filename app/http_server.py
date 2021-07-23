import asyncio
import json
import uuid
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

from producers.order_producer import OrderProducer

from models.user import User
from models.order import Order


class HttpHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.order_producer = OrderProducer()
        super().__init__(request, client_address, server)


    def _write_response(self, status, message):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'message': message}).encode('utf8'))

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
            self._write_response(400, 'Invalid Parameters')
            return False

        return {'name': name, 'email': email, 'total': float(total)}

    def do_GET(self):
        params = self.get_url_params()

        if not params:
            return

        user = User(
            params['name'],
            params['email'],
            str(uuid.uuid4()),
        )
        order = Order(
            str(uuid.uuid4()),
            user,
            params['total'],
        )
        
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.order_producer.send(order))

        self._write_response(201, 'Order created')


def run():
    server = HTTPServer(
        ('', 8080),
        HttpHandler
    )

    server.serve_forever()

if __name__ == '__main__':
    run()