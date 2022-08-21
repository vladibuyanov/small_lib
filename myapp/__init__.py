from flask import Flask
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# Import database
from myapp.extensions import db, migrate

# Import models
from myapp.models.books import Books
from myapp.models.user import User

# Import Admin views
from .admin.main import DashBoardView, MyModelView

# Import routes
from .routes.main import main
from .routes.user import users
from .routes.user_log import user_log
from .routes.user_registration import user_registration
from .routes.book import book


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
    admin.add_view(MyModelView(Books, db.session, name='Books'))

    # Routes
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(user_log)
    app.register_blueprint(user_registration)
    app.register_blueprint(book)

    return app
