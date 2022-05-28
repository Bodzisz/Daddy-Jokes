DEVELOPMENT = 'development'


class Config(object):
    SECRET_KEY = '5f352388884c22463451387a0aec5d2f'
    HANDLER = "RotatingFileHandler"
    DEBUG = True
    TESTING = True
    ENV = DEVELOPMENT
    # MONGO_URI = 'mongodb+srv://kacper_wojcicki:polskagurom@cluster0.wyaxf.mongodb.net/test_db?retryWrites=true&w=majority'
    MONGO_HOST = 'mongo'
    MONGO_PORT = 27017
    MONGO_USERNAME = 'flaskapp'
    MONGO_PASSWORD = 'password'
    MONGO_DB_NAME = 'test'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flaskapp:password@mysql:3306/users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
