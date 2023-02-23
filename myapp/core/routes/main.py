from flask import Blueprint, render_template, request

from myapp import Book, User

from myapp.core.functions.main import search_func

main = Blueprint('main', __name__)
template_folder = 'pages/main'


@main.route('/', methods=['GET'])
def main_view():
    template = f'{template_folder}/index.html'
    return render_template(template)


@main.route('/search', methods=['GET', 'POST'])
def search_view():
    template = f'{template_folder}/search.html'
    data = search_func(request)

    if request.method == 'GET':
        return render_template(template, data=data)
    else:
        return render_template(template, data=data[0], request=request, books=data[1], users=data[2])


@main.route('/users', methods=['GET'])
def index_users():
    template = f'{template_folder}/users.html'
    return render_template(template, user_res=User.query.all())


@main.route('/books', methods=['GET'])
def index_books():
    template = f'{template_folder}/books.html'
    return render_template(template, books_res=Book.query.all())
