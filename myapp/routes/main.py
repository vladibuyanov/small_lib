from flask import Blueprint, render_template

from myapp import Book, db, User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    users = db.session.query(User).all()[:3]
    books = db.session.query(Book).all()[:3]
    return render_template('main/index.html', user_res=users, books_res=books)


@main.route('/users', methods=['GET'])
def index_users():
    users = db.session.query(User).all()
    return render_template('main/users.html', user_res=users)


@main.route('/books', methods=['GET'])
def index_books():
    books_res = db.session.query(Book).all()
    return render_template('main/books.html', books_res=books_res)
