from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime
from myapp import Book, db, User, Exchange

books = Blueprint('books', __name__)

methods = ['GET', 'POST']
base_url = '/book'

template_folder = 'pages/book'


@books.route(f'{base_url}/add', methods=methods)
@login_required
def book_add():
    template = f'{template_folder}/add.html'

    if request.method == 'GET':
        return render_template(template)
    else:
        book_from_page = Book(
            title=request.form['book'],
            author=request.form['author'],
            about=request.form['about'],
            year_of_publication=request.form['year_of_publication'],
            owner=current_user.id
        )
        try:
            db.session.add(book_from_page)
            db.session.commit()
            return redirect(url_for('users.page', user_id=current_user.id))
        except Warning:
            db.session.rollback()
            flash('Something is going wrong')
            return render_template(template)


@books.route(f'{base_url}/change_info/<int:book_page_id>', methods=methods)
@login_required
def change_info(book_page_id):
    template = f'{template_folder}/change_info.html'
    book_for_change = Book.query.filter_by(id=book_page_id).first()

    if request.method == 'GET':
        return render_template(template, book_for_change=book_for_change)
    else:
        if request.form['title']:
            book_for_change.title = request.form['title']
        if request.form['year_of_publication']:
            book_for_change.year_of_publication = request.form['year_of_publication']
        if request.form['author']:
            book_for_change.author = request.form['author']
        if request.form['about']:
            book_for_change.about = request.form['about']
        try:
            db.session.commit()
            return redirect(url_for('users.page', user_id=current_user.id))
        except Warning:
            db.session.rollback()
            flash('Something going wrong')
            return render_template('book/change_info.html', book_for_change=book_for_change)


@books.route(f'{base_url}/exchange_request/<int:book_id>', methods=methods)
@login_required
def exchange_request(book_id):
    new_exchange = Exchange(
        user_id=Book.query.get(book_id).owner,
        book_id=book_id,
        requester_id=current_user.id,
        status='pending'
    )
    db.session.add(new_exchange)
    db.session.commit()

    return redirect(url_for('users.page', user_id=current_user.id))


@books.route(f'{base_url}/accept_request/<int:exchange_id>', methods=methods)
@login_required
def accept_request_view(exchange_id):
    accept_request = Exchange.query.get(exchange_id)

    # Change
    book_for_give = Book.query.get(accept_request.book_id)
    book_for_give.user_id = accept_request.requester_id

    accept_request.status = 'accepted'
    accept_request.accepted_date = datetime.today()

    db.session.commit()
    return redirect(url_for('users.page', user_id=current_user.id))


@books.route(f'{base_url}/give_back/<int:book_id>')
@login_required
def give_back(book_id):
    book_give_back = Book.query.get(book_id)
    book_give_back.user_id = current_user.id

    end_of_exchange = Exchange.query.filter_by(book_id=book_id)
    end_of_exchange = end_of_exchange.order_by(Exchange.created_date.desc()).first()

    end_of_exchange.status = 'done'
    end_of_exchange.return_date = datetime.today()

    try:
        db.session.commit()
    except Warning:
        db.session.rollback()
    finally:
        return redirect(url_for('users.page', user_id=current_user.id))


@books.route(f'{base_url}/delete/<int:book_page_id>')
@login_required
def delete_book(book_page_id):
    book_for_delete = Book.query.filter_by(id=book_page_id).first()

    try:
        db.session.delete(book_for_delete)
        db.session.commit()
    except Warning:
        db.session.rollback()
    finally:
        return redirect(url_for('users.page', user_id=current_user.id))
