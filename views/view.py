from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from db.mongo_db import mongo

view = Blueprint('view', __name__, template_folder='templates',
                 static_folder='static')

students_collection = mongo.students


@view.route("/")
def home():
    return render_template('index.html')


@view.route("/dashboard")
@login_required
def dashboard():
    username = current_user.username
    return render_template("dashboard.html", username=username)


@view.route("/list")
def student_list():
    students = students_collection.find()
    return render_template("list.html", students=students)


@view.route("/insert_test")
def insert_test():
    students_collection.insert_one(
        {
            'first_name': 'Kacper',
            'last_name': 'Wojcicki',
            'index': 123456
        })
    return redirect('/')
