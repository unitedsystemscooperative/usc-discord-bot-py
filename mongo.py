import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
conn_string = os.getenv('MONGO_CONN')


def get_value(key):
    with MongoClient(conn_string) as client:
        collection = client.usc.discordKeys
        doc = collection.find_one({'key': key})
        if doc:
            return doc['value']


def set_value(key, value):
    try:
        with MongoClient(conn_string) as client:
            collection = client.usc.discordKeys
            collection.update_one(
                {'key': key}, {'$set': {'value': value}}, upsert=True)
    except:
        print('Unexpected error while setting value')
        raise
