from flask import Blueprint, render_template

from myapp import Book, db, User

main = Blueprint('main', __name__)
template_folder = 'pages/main'


@main.route('/', methods=['GET', 'POST'])
def index():
    template = f'{template_folder}/index.html'
    users = db.session.query(User).all()[:3]
    books = db.session.query(Book).all()[:3]

    return render_template(template, user_res=users, books_res=books)


@main.route('/users', methods=['GET'])
def index_users():
    template = f'{template_folder}/users.html'
    users = db.session.query(User).all()

    return render_template(template, user_res=users)


@main.route('/books', methods=['GET'])
def index_books():
    template = f'{template_folder}/books.html'
    books_res = db.session.query(Book).all()

    return render_template(template, books_res=books_res)
