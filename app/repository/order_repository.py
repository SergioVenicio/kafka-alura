import os

from models.order import Order

from .base_repository import BaseRepository


class OrderRepository(BaseRepository):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        db_file = os.path.join(path, '../../orders.db')
        super().__init__(db_file)

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE orders (
            id varchar(255) primary key,
            user varchar(255),
            total decimal(10, 5)
        );
        """)
        self.connection.commit()

    def create_order(self, order: Order):
        print(f'Creating order: {order}')

        sql = f"""
        INSERT INTO orders (id, user, total)
            VALUES ("{order.id}", "{order.user.id}", {order.total});
        """
        self.cursor.execute(sql)
        self.connection.commit()

    def get_order_by_id(self, id):
        sql = f"""
        SELECT COUNT(id) FROM orders WHERE id = "{id}";
        """

        self.cursor.execute(sql)
        return self.cursor.fetchone()[0] > 0
