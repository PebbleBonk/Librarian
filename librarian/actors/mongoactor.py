from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from librarian.actors.actor import Actor


class MongoActor(Actor):
    """ An actor to upload data into a remote mongoDB

        The url to establish the mongo client is formed as:
        'mongodb://{usr}:{pwd}@{url}/{db}'.
        NOTE: Alternatively, this url could be the only argument?

        Args:
            usr (str): Username for the mongoDB connection
            pwd (str): Password for the mongoDB connection
            url (str): mongoDB connection url
            db (str): mongoDB database name to which data is uploaded
            col (str): mongoDB collection name to which data is uploaded
    """
    def __init__(self, usr, pwd, url, db, col):
        super().__init__()
        self.description = "Uploads data to mongoDB"
        # Create mLab string:
        mongo_str =  f'mongodb://{usr}:{pwd}@{url}/{db}'
        mongo_str += '?retrywrites=false'

        # Set up the general client:
        self.client = MongoClient(mongo_str)
        self.db = self.client[db]
        self.col = self.db[col]

    def act(self, data, uid):
        data["uid"] = uid
        return self.put_one(data)

    def put_one(self, data):
        """ Insert data to collection.

            Args:
                data (list of dicts): Data to insert
                validate (bool): Whether to validate the data

            Return (list):
                List of succesfully inserted objects

            Raise:
                ValueError: During validation if needed

            NOTE: What to do with already existing objects?
        """
        assert isinstance(data, dict), "MongoActor: Data was not a dict"

        if not data:
            print("Empty data, returning")
            return []

        # Insert to the collection:
        result = self.col.insert_one(data)
        return result

    def get_latest_data(self, q={}, n=1):
        """ Query the database and return the n latest documents

            Args:
                user_id (int): user_id for query
                project (str): project name for query

            Return (list of dicts):
                List of n last found items, empty list if no such project
                exists.

            Raise:
                ValueError on invalid user_id

        """
        docs = self.col.find(q).sort([('_id', -1)]).limit(n)

        # XXX: remove ObjectId:
        docs = [d for d in docs]
        for obj in docs:
            del obj['_id']

        return list(docs)

    def get_single(self, oid):
        """ Query for one specific record
        """
        doc = self.col.find_one({'_id': ObjectId(oid)}, {'_id':0})
        return doc

    def get_ids(self, q, n=1):
        """ Query database for the ids only. Used for history

            NOTE: Consider effects of using the explicit _id
        """
        docs = self.col.find(q).sort([('_id', -1)]).limit(n)

        for d in docs:
            d['_id'] = str(d['_id'])
            ret.append(d)

        return ret

