from abc import ABC, abstractmethod

import sqlite3


class BaseRepository(ABC):
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        try:
            self.create_table()
        except Exception:
            pass

    def __del__(self):
        self.connection.close()

    @abstractmethod
    def create_table(self):
        ...