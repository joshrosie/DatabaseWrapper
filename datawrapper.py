import json
import os
from pymongo import MongoClient


def load_data_mongo():
    client = MongoClient('localhost',27017)
    if('MSD' not in client.list_database_names()):
        db=client['MSD']
        collection = db['songs']

        for file in os.listdir("./data/"):
            f = open('./data/' + file)
            data = json.load(f)
            collection.insert_one(data)
            f.close()
        print('Song data loaded')
    else:
        print('MSD Data already loaded')
    client.close()

def helper(data):
    new_data = []
    for i in data:
        new_data.append(tuple(i))
    
    return set(new_data)
