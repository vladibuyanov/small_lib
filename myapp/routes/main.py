from flask import Blueprint, render_template

from extensions import db
from models.user import User
from models.book import Book

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    all_users = db.session.query(User).all()[:3]
    books_res = db.session.query(Book).all()[:3]
    return render_template('index.html', user_res=all_users, books_res=books_res)
