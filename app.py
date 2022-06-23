from flask import Flask
from config import configurations
from views.auth_views import auth as auth_blueprint
from db.user_db import db
from views.auth_views import bcrypt, login_manager
from views.main_views import main as main_blueprint
from views.joke_views import jokes as jokes_blueprint
from db.mongo_db import mongo_client
from config.configurations import MongoConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(configurations.Config)

    if MongoConfig.MONGO_DB_NAME not in mongo_client.list_database_names():
        mongo_client[MongoConfig.MONGO_DB_NAME]

    bcrypt.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(jokes_blueprint, url_prefix='/jokes')

    return app


def setup_database(app):
    with app.app_context():
        db.create_all()


if __name__ == "__main__":
    app = create_app()
    setup_database(app)
    app.run(host='0.0.0.0')
