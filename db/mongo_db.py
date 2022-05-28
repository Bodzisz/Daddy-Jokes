from flask_pymongo import PyMongo

mongo = PyMongo()
students_collection = mongo.db.students
