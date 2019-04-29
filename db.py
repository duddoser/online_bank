import sqlite3


class DB:

    def __init__(self, value):
        conn = sqlite3.connect(value, check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()
