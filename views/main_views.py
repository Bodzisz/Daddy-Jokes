from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from db.mongo_db import mongo
from random import randrange

main = Blueprint('view', __name__, template_folder='templates',
                 static_folder='static')

jokes_collection = mongo.jokes


@main.route("/")
def home():
    username = current_user.username if current_user.is_authenticated else None
    is_authenticated = current_user.is_authenticated
    random_joke = get_random_joke()
    return render_template('index.html', username=username, is_authenticated=is_authenticated, random_joke=random_joke)


def get_random_joke():
    try:
        rand = randrange(jokes_collection.count_documents({}))
    except ValueError:
        return None
    return jokes_collection.find()[rand]

