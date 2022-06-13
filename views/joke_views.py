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
                'datetime': str(datetime.datetime.now()),
                'likes': []
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

    sorting = args.get('sorting', None)
    descending = args.get('descending', False)
    jokes_list = sort_jokes(jokes_list, sorting, descending)

    return render_template("list.html", jokes=jokes_list, username=username, is_authenticated=is_authenticated)


def filter_jokes(full_joke_list, field, value):
    filtred = []
    for single_joke in full_joke_list:
        if value.lower() in single_joke[field].lower():
            filtred.append(single_joke)
    return filtred


def sort_jokes(full_jokes_list, sorting, descending):
    result = []
    if sorting is not None:
        if descending == 'False':
            descending = False
        else:
            descending = True
        if sorting == 'date':
            result = sorted(full_jokes_list, key=lambda joke: joke['datetime'], reverse=descending)
        elif sorting == 'likes':
            result = sorted(full_jokes_list, key=lambda joke: len(joke['likes']), reverse=descending)
    else:
        result = sorted(full_jokes_list, key=lambda joke: joke['datetime'], reverse=True)
    return result


@jokes.route("/<joke_id>")
def joke(joke_id):
    username = current_user.username if current_user.is_authenticated else None
    selected_joke = jokes_collection.find_one({"_id": ObjectId(joke_id)})
    likes = len(selected_joke['likes'])
    user_liked = True if username in selected_joke['likes'] else False
    if selected_joke is not None:
        return render_template("joke.html", joke=selected_joke, username=username,
                               is_authenticated=current_user.is_authenticated,
                               likes=likes, user_liked=user_liked)
    else:
        return abort(404)


@jokes.route("/search", methods=['GET', 'POST'])
def search():
    select = request.form.get('search_select', None)
    value = request.form.get('value', None)
    sorting = request.form.get('sorting', None)
    descending = request.form.get('descending', 'False')
    args_string = "?"
    for key, text in [('sorting', sorting), ('descending', descending)]:
        if value != 'None':
            args_string += key + "=" + text + "&"

    if value == "":
        return redirect(url_for('jokes.joke_list') + args_string)
    return redirect(url_for('jokes.joke_list') + '/?' + args_string + select + '=' + value)


@jokes.route("/edit/<joke_id>", methods=['GET', 'POST'])
@login_required
def edit_joke(joke_id):
    selected_joke = jokes_collection.find_one({"_id": ObjectId(joke_id)})
    if selected_joke is not None:
        if selected_joke['author'] == current_user.username:
            form = AddJokeForm()

            if form.validate_on_submit():
                jokes_collection.update_one(
                    {
                        '_id': ObjectId(joke_id)
                    },
                    {
                        "$set": {
                            'name': form.name.data,
                            'content': form.content.data,
                        }
                    },
                    upsert=False
                )
                return redirect(url_for('jokes.joke_list') + "/" + str(selected_joke['_id']))
            form.name.data = selected_joke['name']
            form.content.data = selected_joke['content']
            form.submit.label.text = "Edit"
            return render_template('add-joke.html', form=form)
        else:
            abort(403)
    else:
        return abort(404)


@jokes.route("/toggle/<joke_id>")
@login_required
def joke_like_toggle(joke_id):
    selected_joke = jokes_collection.find_one({"_id": ObjectId(joke_id)})
    username = current_user.username
    if username in selected_joke['likes']:
        selected_joke['likes'].remove(username)
        user_liked = False
    else:
        user_liked = True
        selected_joke['likes'].append(username)
    jokes_collection.update_one(
        {
            '_id': ObjectId(joke_id)
        },
        {
            "$set": {
                'likes': selected_joke['likes']
            }
        },
        upsert=False
    )
    from_list = request.args.get('from_list', None)
    if from_list is None:
        return render_template("joke.html", joke=selected_joke, username=username, is_authenticated=True,
                               likes=len(selected_joke['likes']), user_liked=user_liked)
    else:
        jokes_list = jokes_collection.find()
        return render_template("list.html", jokes=jokes_list, username=username, is_authenticated=True,
                               likes=len(selected_joke['likes']))


@jokes.route("/sort", methods=["POST"])
def sort():
    sorting = request.form.get('sorting', None)
    descending = request.form.get('descending', None)
    name_search = request.form.get('name_search', None)
    author_search = request.form.get('author_search', None)
    content_search = request.form.get('content_search', None)
    args_string = '?'
    for key, value in [('name', name_search), ('author', author_search), ('content', content_search)]:
        if value != 'None':
            args_string += key + '=' + value + "&"
    return redirect(url_for('jokes.joke_list') + '/' + args_string + 'sorting=' + sorting + '&descending=' + descending)
