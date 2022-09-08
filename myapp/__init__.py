from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from myapp.core.extensions import db, migrate
from myapp.core.models.book import Book
from myapp.core.models.user import User
from myapp.core.models.genre import Genre

from myapp.core.admin.main import DashBoardView, MyModelView

from myapp.core.routes.main import main
from myapp.core.routes.user import users
from myapp.core.routes.book import books
from myapp.core.routes.user_log import user_log
from myapp.core.routes.user_registration import user_registration


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    login_manager = LoginManager(app, db)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    # Admin panel
    admin = Admin(app, name="Small Lib", template_mode='bootstrap4', endpoint='admin', index_view=DashBoardView())
    admin.add_view(ModelView(User, db.session, name='Users'))
    admin.add_view(MyModelView(Book, db.session, name='Books'))
    admin.add_view(MyModelView(Genre, db.session, name='Genre'))

    # Routes
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(user_log)
    app.register_blueprint(user_registration)
    app.register_blueprint(books)

    return app
