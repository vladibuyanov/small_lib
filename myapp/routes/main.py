from flask import Blueprint, render_template

from myapp import Books, db, User

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index():
    users = db.session.query(User).all()[:3]
    books = db.session.query(Books).all()[:3]
    return render_template('index.html', user_res=users, books_res=books)


# @main.route('/users', methods=['GET', 'POST'])
# def index_users():
#     users = db.session.query(User).all()
#     return render_template('index.html', user_res=users)
#
#
# @main.route('/books', methods=['GET', 'POST'])
# def index_books():
#     books_res = db.session.query(Books).all()
#     return render_template('index.html', books_res=books_res)
