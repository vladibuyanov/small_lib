from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from myapp.core.functions.book import book_add_func, book_change_info_func, book_exchange_request_func
from myapp.core.functions.book import book_accept_request_func, book_give_back_func, book_delete_func

books = Blueprint('books', __name__)

methods = ['GET', 'POST']

base_url = '/book'
redirect_page = 'users.user_page_view'
template_folder = 'pages/book'


@books.route(f'{base_url}/add', methods=methods)
@login_required
def book_add_view():
    template = f'{template_folder}/add.html'

    if request.method == 'GET':
        form = book_add_func(request, current_user)
        return render_template(template, form=form)
    else:
        book_add_func(request, current_user)
        return redirect(url_for(redirect_page, user_id=current_user.id))


@books.route(f'{base_url}/change_info/<int:book_page_id>', methods=methods)
@login_required
def book_change_info_view(book_page_id):
    template = f'{template_folder}/change_info.html'

    if request.method == 'GET':
        form = book_change_info_func(request, book_page_id)
        return render_template(template, form=form)
    else:
        book_change_info_func(request, book_page_id)
        return redirect(url_for(redirect_page, user_id=current_user.id))


@books.route(f'{base_url}/exchange_request/<int:book_id>', methods=methods)
@login_required
def book_exchange_request_view(book_id):
    book_exchange_request_func(book_id, current_user)
    return redirect(url_for(redirect_page, user_id=current_user.id))


@books.route(f'{base_url}/accept_request/<int:exchange_id>', methods=methods)
@login_required
def book_accept_request_view(exchange_id):
    book_accept_request_func(exchange_id)
    return redirect(url_for(redirect_page, user_id=current_user.id))


@books.route(f'{base_url}/give_back/<int:book_id>')
@login_required
def book_give_back_view(book_id):
    book_give_back_func(book_id)
    return redirect(url_for(redirect_page, user_id=current_user.id))


@books.route(f'{base_url}/delete/<int:book_id>')
@login_required
def book_delete_view(book_id):
    book_delete_func(book_id)
    return redirect(url_for(redirect_page, user_id=current_user.id))
