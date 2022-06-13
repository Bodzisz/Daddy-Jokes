from pymongo import MongoClient
from config.configurations import MongoConfig


mongo_client = MongoClient(host=MongoConfig.MONGO_HOST,
                           port=MongoConfig.MONGO_PORT,
                           username=MongoConfig.MONGO_USERNAME,
                           password=MongoConfig.MONGO_PASSWORD)
mongo = mongo_client[MongoConfig.MONGO_DB_NAME]
