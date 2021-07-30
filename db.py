from pymongo import MongoClient


class DB:
    def __init__(self, database) -> None:
        super().__init__()
        self.connection_string = "mongodb://mongo/" + database
        self.client = MongoClient(self.connection_string)
        self.database = self.client[database]

    def get_collection(self, collection_name):
        return self.database[collection_name]
