from flask import Flask
from flask_login import LoginManager

from .extensions import db, migrate
from .config import *

# import routes
from .routes.main import main
from .routes.user import user
from .routes.login import login
from .routes.logout import logout
from .routes.user_registration import user_registration
from .routes.admin import admin
from .routes.book import book

# import models
from .models.user import User
from .models.books import Books


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
    app.config['DEBUG'] = debug

    db.init_app(app)
    migrate.init_app(app)
    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Routes
    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(user)
    app.register_blueprint(login)
    app.register_blueprint(logout)
    app.register_blueprint(user_registration)
    app.register_blueprint(book)


    return app
