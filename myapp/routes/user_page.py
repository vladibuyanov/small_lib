from flask import Blueprint, render_template
from flask_login import login_required

from ..extensions import db
from ..models.user import User
from ..models.books import Books

user_page = Blueprint('user_page', __name__)


# User dynamic page
@user_page.route('/user_page/<int:user_id>')
def user(user_id):
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
