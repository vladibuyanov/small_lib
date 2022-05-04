from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from werkzeug.security import generate_password_hash

from ..extensions import db
from ..models.user import User
from ..models.books import Books

user = Blueprint('user', __name__)


@user.route('/user/<int:user_id>')
def page(user_id):
    # Take all user for dynamic page
    all_user_dp = db.session.query(User).all()
    # All books of user from page
    user_books = Books.query.filter_by(owner=all_user_dp[user_id - 1].id).all()
    # All books
    all_books = Books.query.all()
    return render_template('user_page.html',
                           user_res=all_user_dp[user_id - 1],
                           users=all_user_dp,
                           user_books=user_books,
                           all_books=all_books)


@user.route('/user/user_settings/<int:user_id>', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    user_settings = User.query.filter_by(id=user_id).first()
    if request.method == "POST":
        name = request.form['settings_name']
        email = request.form['settings_email']
        password = request.form['settings_password']
        user_settings.name = name
        user_settings.email = email
        user_settings.password = generate_password_hash(password, method='sha256')
        try:
            db.session.commit()
            return redirect(url_for('user.page', user_id=1))
        except Warning:
            db.session.rolback()
            flash('Something going wrong')
            return redirect(url_for('main.index'))
    return render_template('user_settings.html', user_settings=user_settings)
