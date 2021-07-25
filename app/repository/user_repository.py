import os

from exceptions.user import UserNotFoundException

from .base_repository import BaseRepository

from models.user import User


class UserRepository(BaseRepository):
    def __init__(self):
        path = os.path.dirname(os.path.abspath(__file__))
        db_file = os.path.join(path, '../../users.db')
        super().__init__(db_file)

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE users (
            id varchar(255) primary key,
            name varchar(255),
            email varchar(255) unique
        );
        """)
        self.connection.commit()

    def create_user(self, user: User):
        print(f'Creating user: {user}')
        sql = f"""
        INSERT INTO users (id, name, email)
            VALUES ("{user.id}", "{user.name}", "{user.email}");
        """
        self.cursor.execute(sql)
        self.connection.commit()

    def get_users(self):
        print(f'Get users')
        sql = f"""
        SELECT
            name
            , email
            , id
        FROM users;
        """

        self.cursor.execute(sql)
        return [
            User(row[0], row[1], row[2])
            for row in self.cursor.fetchall()
        ]

    def get_user_by_id(self, user_id):
        sql = f"""
        SELECT 
            name
            , email
            , id
        FROM users WHERE id = "{user_id}"
        LIMIT 1;
        """

        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if not row:
            raise UserNotFoundException('User not found')

        return User(row[0], row[1], row[2])

    def get_user_by_email(self, email):
        sql = f"""
        SELECT 
            name
            , email
            , id
        FROM users WHERE email = "{email}"
        LIMIT 1;
        """

        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if not row:
            return

        return User(row[0], row[1], row[2])
