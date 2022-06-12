from bson import ObjectId
from flask import Blueprint, render_template, redirect, request, url_for, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Length
from db.mongo_db import mongo
import datetime

jokes = Blueprint('jokes', __name__, template_folder='templates',
                  static_folder='static')

jokes_collection = mongo.jokes


class AddJokeForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(
        min=2, max=30)], render_kw={"placeholder": "Joke name"})

    content = TextAreaField(render_kw={"placeholder": "Joke content"}, validators=[InputRequired(), Length(
        min=2)])

    submit = SubmitField("Add")


@jokes.route('/add', methods=['GET', 'POST'])
@login_required
def add_joke():
    form = AddJokeForm()

    if form.validate_on_submit():
        jokes_collection.insert_one(
            {
                'name': form.name.data,
                'content': form.content.data,
                'author': current_user.username,
                'datetime': str(datetime.datetime.now())
            })
        return redirect(url_for('jokes.joke_list'))
    return render_template('add-joke.html', form=form)


@jokes.route('/delete/<joke_id>')
@login_required
def delete_joke(joke_id):
    selected_joke = jokes_collection.find_one({"_id": ObjectId(joke_id)})
    if selected_joke is not None:
        if selected_joke['author'] == current_user.username:
            jokes_collection.delete_one({"_id": ObjectId(joke_id)})
            return redirect(url_for('jokes.joke_list'))
        else:
            abort(403)
    else:
        return abort(404)


@jokes.route("/")
def joke_list():
    username = current_user.username if current_user.is_authenticated else None
    is_authenticated = current_user.is_authenticated

    jokes_list = jokes_collection.find()

    valid_args = ['author', 'name', 'content']
    args = request.args
    for arg in args:
        if arg in valid_args:
            jokes_list = filter_jokes(jokes_list, arg, args[arg])

    jokes_list = sorted(jokes_list, key=lambda joke: joke['datetime'], reverse=True)

    return render_template("list.html", jokes=jokes_list, username=username, is_authenticated=is_authenticated)


def filter_jokes(full_joke_list, field, value):
    filtred = []
    for single_joke in full_joke_list:
        if value.lower() in single_joke[field].lower():
            filtred.append(single_joke)
    return filtred


@jokes.route("/<joke_id>")
def joke(joke_id):
    username = current_user.username if current_user.is_authenticated else None
    selected_joke = jokes_collection.find_one({"_id": ObjectId(joke_id)})
    if selected_joke is not None:
        return render_template("joke.html", joke=selected_joke, username=username)
    else:
        return abort(404)


@jokes.route("/search", methods=['GET', 'POST'])
def search():
    select = request.form.get('search_select', None)
    value = request.form.get('value', None)
    if value == "":
        return redirect(url_for('jokes.joke_list'))
    return redirect(url_for('jokes.joke_list') + '/?' + select + '=' + value)
