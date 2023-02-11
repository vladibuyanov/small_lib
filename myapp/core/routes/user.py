from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

from myapp import Book, db, User

users = Blueprint('users', __name__)

methods = ['GET', 'POST']
base_url = '/user'


# TODO: Сократить кол-во запросов к бд
@users.route(f'{base_url}/<int:user_id>')
def page(user_id):
    template = 'pages/user/user_page.html'

    all_users = User.query.all()
    user = User.query.filter_by(id=user_id).first()
    user_books = Book.query.filter_by(owner=user_id).all()
    borrowed_books = Book.query.filter(Book.user_id == user_id, Book.owner != user_id).all()

    return render_template(template, users=all_users, user=user,
                           user_books=user_books, borrowed_books=borrowed_books)


@users.route(f'{base_url}/user_settings/<int:user_id>', methods=methods)
@login_required
def settings(user_id):
    template = 'pages/user/user_settings.html'

    redirect_page = 'main.index'
    user = User.query.filter_by(id=user_id).first()

    if current_user.id != user_id:
        return redirect(url_for(redirect_page))
    else:
        if request.method == 'GET':
            return render_template(template, user_settings=user)
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
            try:
                db.session.commit()
                return redirect(url_for(redirect_page, user_id=user_id))
            except Warning:
                db.session.rolback()
                flash('Something going wrong')
                return redirect(url_for(redirect_page))


@users.route(f'{base_url}/user_settings/delete/<int:user_id>', methods=methods)
@login_required
def delete(user_id):
    redirect_page = 'main.index'

    logout_user()
    delete_user = User.query.filter_by(id=user_id).first()

    try:
        db.session.delete(delete_user)
        db.session.commit()
    except Warning:
        db.session.rollback()
    finally:
        return redirect(url_for(redirect_page))
