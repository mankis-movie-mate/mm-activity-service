from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class MongoDB:
    def __init__(self, db_name: str, host: str = 'localhost', port: int = 27017, username: str = None, password: str = None):
        if username and password:
            uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}"
        else:
            uri = f"mongodb://{host}:{port}/{db_name}"

        self.client = MongoClient(uri)
        self.db = self.client[db_name]


    def test_connection(self):
        try:
            self.client.get_database(self.db.name).command("ping")
            return True
        except ConnectionFailure:
            return False


    def get_collection(self, name: str):
        return self.db[name]


    def close_connection(self):
        self.client.close()