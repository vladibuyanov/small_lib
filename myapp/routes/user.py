from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models.user import User
from ..models.books import Books

users = Blueprint('users', __name__)


@users.route('/user/<int:user_id>')
def page(user_id):
    # Take all user for dynamic page and all books of user from page
    all_user_dp = db.session.query(User).all()
    user_books = Books.query.filter_by(owner=user_id).all()

    # Books that user took
    took_book = []
    all_user_books = Books.query.filter_by(user_id=user_id).all()
    for book in all_user_books:
        if book.user_id == user_id and user_id != book.owner:
            took_book.append(book)

    return render_template('user/user_page.html',
                           user_res=all_user_dp[user_id - 1],
                           users=all_user_dp,
                           user_books=user_books,
                           took_book=took_book,
                           number_of_took_book=len(took_book)
                           )


@users.route('/user/user_settings/<int:user_id>', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    user_settings = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        if request.form['settings_name']:
            user_settings.name = request.form['settings_name']
        if request.form['settings_email']:
            user_settings.email = request.form['settings_email']
        if request.form['settings_password']:
            user_settings.password = generate_password_hash(request.form['settings_password'], method='sha256')
        try:
            db.session.commit()
            return redirect(url_for('users.page', user_id=1))
        except Warning:
            db.session.rolback()
            flash('Something going wrong')
            return redirect(url_for('main.index'))
    return render_template('user/user_settings.html', user_settings=user_settings)
