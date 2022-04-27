from flask import Blueprint, render_template

from ..extensions import db
from ..models.user import User
from ..models.books import Books

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    # Take all users
    all_users = db.session.query(User).all()
    # Take all books
    books_res = db.session.query(Books).all()
    return render_template('index.html', user_res=all_users, books_res=books_res)
