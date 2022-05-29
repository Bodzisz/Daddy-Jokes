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

    content = TextAreaField(render_kw={"placeholder": "Joke content"})

    submit = SubmitField("Add")


@login_required
@jokes.route('/add', methods=['GET', 'POST'])
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


@login_required
@jokes.route('/delete/<joke_id>')
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


@jokes.route("/list")
def joke_list():
    author = request.args.get('author', None)
    if author is None:
        jokes_list = jokes_collection.find()
    else:
        jokes_list = jokes_collection.find({"author": author})
    return render_template("list.html", jokes=jokes_list)
