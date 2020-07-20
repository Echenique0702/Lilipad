import pymongo

conection = pymongo.MongoClient('database', 27017)
database = conection['lilipad']


def insert_data(collection: str, data: dict):
    insert = database[collection].insert_one(data)
    return 'Ok'


def find_data(collection: str, data: dict):
    find = database[collection].find_one(data)
    return find


def insert_many(collection: str, data: list):
    insert = database[collection].insert_many(data)
    return 'Ok'


def get_collection(collection: str):
    find = database[collection].find()
    return find


def drop(database: str):
    drop_database = conection.drop_database(database)
    return drop_database
