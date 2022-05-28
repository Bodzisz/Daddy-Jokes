from pymongo import MongoClient

mongo_client = MongoClient(host='mongo', port=27017,
                           username='flaskapp',
                           password='password',
                           authSource='admin')
mongo = mongo_client["test"]
