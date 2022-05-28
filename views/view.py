from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

view = Blueprint('view', __name__, template_folder='templates',
                 static_folder='static')


@view.route("/")
def home():
    return render_template('index.html')


@view.route("/dashboard")
@login_required
def dashboard():
    username = current_user.username
    return render_template("dashboard.html", username=username)
