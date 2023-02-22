from werkzeug.security import generate_password_hash
from flask_login import logout_user

from myapp import db, Book, User, Exchange


def user_page_func(user_id):
    all_users = User.query.all()
    all_books = Book.query.all()

    user = all_users[user_id - 1]
    user_books = [book for book in all_books if book.owner == user_id]
    borrowed_books = [book for book in all_books if book.owner != user_id and book.user_id == user_id]

    return all_users, user, user_books, borrowed_books


def user_exchange_history_func(user_id):
    all_users = User.query.all()
    all_books = Book.query.all()

    my_requests = Exchange.query.filter_by(requester_id=user_id)
    users_requests = Exchange.query.filter_by(user_id=user_id)

    return all_users, all_books, users_requests, my_requests


def user_settings_func(request, user_id):
    user = User.query.get(user_id)
    if request.method == 'GET':
        return user
    else:
        if request.form['settings_name']:
            user.name = request.form['settings_name']
        if request.form['settings_email']:
            user.email = request.form['settings_email']
        if request.form['settings_place']:
            user.place = request.form['settings_place']
        if request.form['settings_password']:
            user.password = generate_password_hash(
                request.form['settings_password'],
                method='sha256'
            )
        db.session.commit()


def user_delete_func(user_id):
    logout_user()
    delete_user = User.query.get(user_id)
    db.session.delete(delete_user)
    db.session.commit()
