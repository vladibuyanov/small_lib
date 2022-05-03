from flask import Blueprint, render_template
from flask_login import login_required

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


@user.route('/user/user_settings/<int:user_id>')
@login_required
def settings(user_id):
    return render_template('user_settings.html')
