from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user
from db.mongo_db import mongo
import datetime

main = Blueprint('view', __name__, template_folder='templates',
                 static_folder='static')

jokes_collection = mongo.jokes


@main.route("/")
def home():
    username = current_user.username if current_user.is_authenticated else None
    is_authenticated = current_user.is_authenticated
    return render_template('index.html', username=username, is_authenticated=is_authenticated)


@main.route("/dashboard")
@login_required
def dashboard():
    username = current_user.username
    return render_template("dashboard.html", username=username)

