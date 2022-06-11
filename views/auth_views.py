from flask import Blueprint, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from flask_bcrypt import Bcrypt
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from db.user_db import db
from model.User import User

auth = Blueprint('auth', __name__, template_folder='templates',
                 static_folder='static')

bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "auth.login"


class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    password_confirm = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Retype password"})

    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_user.is_authenticated:
        form = LoginForm()

        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect(url_for('view.home'))
            return render_template('login.html', form=form, password_error=True)
        return render_template('login.html', form=form)
    else:
        return redirect('/')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first() is None:
            if form.password_confirm.data != form.password.data:
                return render_template('register.html', form=form, password_match=False)
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return render_template('register.html', form=form, username_exists=True)

    return render_template('register.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')



