DEVELOPMENT = 'development'


class Config(object):
    SECRET_KEY = '5f352388884c22463451387a0aec5d2f'
    HANDLER = "RotatingFileHandler"
    DEBUG = True
    TESTING = True
    ENV = DEVELOPMENT
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskapp:password@mysql:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10


class ProductionConfig(object):
    DEVELOPMENT = False
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskapp:password@mysql:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE = 10


class MongoConfig(object):
    MONGO_HOST = 'mongo'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'flaskapp'
    MONGO_PASSWORD = 'password'
    MONGO_DB_NAME = 'test'
