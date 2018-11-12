import pymongo

class AuthDB:

    def __init__(self):
        # opens a connection with the local database
        self.client = pymongo.MongoClient()
        self.db = self.client.db
        # naming the collection
        self.collection = self.db.auth

    def insert(self, data):
        try:
            post_id = self.collection.insert_one(data).inserted_id
        except:
            return 'Error'
        return 'Success'