from werkzeug.security import generate_password_hash
from flask_login import logout_user

from myapp.core.forms.user_forms import SettingsForm
from myapp import db, Book, User, Exchange


def query_to_db_all():
    return User.query.all(), Book.query.all()


def user_page_func(user_id):
    db_query = query_to_db_all()

    user = db_query[0][user_id - 1]
    user_books = [book for book in db_query[1] if book.owner == user_id]
    borrowed_books = [book for book in db_query[1] if book.owner != user_id and book.user_id == user_id]

    return db_query[0], user, user_books, borrowed_books


def user_exchange_history_func(user_id):
    db_query = query_to_db_all()

    my_requests = Exchange.query.filter_by(requester_id=user_id).order_by(Exchange.created_date.desc())
    users_requests = Exchange.query.filter_by(user_id=user_id).order_by(Exchange.created_date.desc())

    return db_query[0], db_query[1], users_requests, my_requests


def user_settings_func(request, user_id):
    form = SettingsForm(user_id)
    user = User.query.get(user_id)

    if request.method == 'GET':
        return user, form

    if request.method == 'POST':
        if form.name.data:
            user.name = form.name.data
        if form.email.data:
            user.email = form.email.data
        if form.place.data:
            user.place = form.place.data
        if form.psw.data:
            user.password = generate_password_hash(
                form.psw.data, method='sha256'
            )
        db.session.commit()


def user_delete_func(user_id):
    logout_user()
    delete_user = User.query.get(user_id)
    db.session.delete(delete_user)
    db.session.commit()
