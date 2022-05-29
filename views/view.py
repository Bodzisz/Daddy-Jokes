from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from db.mongo_db import mongo
import datetime

view = Blueprint('view', __name__, template_folder='templates',
                 static_folder='static')

jokes_collection = mongo.jokes


@view.route("/")
def home():
    username = current_user.username if current_user.is_authenticated else None
    is_authenticated = current_user.is_authenticated
    return render_template('index.html', username=username, is_authenticated=is_authenticated)


@view.route("/dashboard")
@login_required
def dashboard():
    username = current_user.username
    return render_template("dashboard.html", username=username)


@view.route("/list")
def student_list():
    jokes = jokes_collection.find()
    return render_template("list.html", jokes=jokes)


@view.route("/insert_test")
def insert_test():
    jokes_collection.insert_one(
        {
            'name': 'Baba',
            'content': 'Wchodzi baba do lekarza, a lekarz też baba',
            'author': "kacper",
            'datetime': str(datetime.datetime.now())
        })
    return redirect('/')
