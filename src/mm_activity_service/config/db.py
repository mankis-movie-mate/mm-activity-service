import logging

from mongoengine import connect, disconnect
from mongoengine.connection import get_connection
from pymongo.errors import ConnectionFailure


class MongoDBConnector:
    def __init__(self, db_name: str, host: str, port: int, username: str = None, password: str = None):
        self.db_name = db_name
        self.host = host
        self.port = port

        connect_params = {
            'db': self.db_name,
            'host': self.host,
            'port': self.port,
        }
        if username and password:
            connect_params['username'] = username
            connect_params['password'] = password
            self.username = username
            self.password = password

        connect(**connect_params)


    def test_connection(self):
        try:
            conn = get_connection()
            conn.admin.command('ping')
            return True
        except ConnectionFailure:
            return False

    def close_connection(self):
        disconnect()