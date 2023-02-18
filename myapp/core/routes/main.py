from flask import Blueprint, render_template, request

from myapp import Book, db, User
from myapp.core.forms.search_form import SearchFrom

main = Blueprint('main', __name__)
template_folder = 'pages/main'


@main.route('/', methods=['GET'])
def index():
    template = f'{template_folder}/index.html'
    res = db.session

    return render_template(template, user_res=res.query(User)[:3], books_res=res.query(Book)[:3])


# TODO: убрать костыль "result"
@main.route('/search', methods=['GET', 'POST'])
def search():
    template = f'{template_folder}/search.html'
    form = SearchFrom()
    data = {'form': form, 'result': None}

    if request.method == 'GET':
        return render_template(template, data=data)
    if form.validate_on_submit():
        searched = form.searched.data

        is_books = Book.query.filter(Book.title.like(f'%{searched}%'))
        is_user = User.query.filter(User.name.like(f'%{searched}%'))

        is_books = is_books.order_by(Book.title).all()
        is_user = is_user.order_by(User.name).all()

        data['result'] = 1

        return render_template(template, data=data, books=is_books, users=is_user)


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
