from flask import Flask
from flask_login import LoginManager
from .admin.admin_main import DashBoardView, MyModelView
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .extensions import db, migrate
from .config import *



# import routes
from .routes.main import main
from .routes.user import users
from .routes.user_log import user_log
from .routes.user_registration import user_registration
from .routes.book import book

# import models
from .models.user import User
from .models.books import Books


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = track_modifications
    app.config['FLASK_ADMIN_SWATCH'] = swath
    app.config['DEBUG'] = debug

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager = LoginManager(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Admin panel
    admin = Admin(app, name="Small Lib", template_mode='bootstrap4', endpoint='admin', index_view=DashBoardView())
    admin.add_view(ModelView(User, db.session, name='Users'))
    admin.add_view(MyModelView(Books, db.session, name='Books'))

    # Routes
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(user_log)
    app.register_blueprint(user_registration)
    app.register_blueprint(book)

    return app
