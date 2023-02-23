from datetime import datetime

from myapp import db, Book, Exchange
from myapp.core.forms.book_forms import BookAddForm, BookChangeForm


def book_add_func(request, current_user):
    form = BookAddForm()

    if request.method == 'GET':
        return form
    else:
        add_new_book = Book(
            title=form.title.data,
            author=form.author.data,
            year_of_publication=form.year_of_publication.data,
            about=form.about.data,
            owner=current_user.id
        )
        db.session.add(add_new_book)
        db.session.commit()


def book_change_info_func(request, book_page_id):
    book_for_change = Book.query.get(book_page_id)
    form = BookChangeForm(book_id=book_page_id)

    if request.method == 'GET':
        return form

    else:
        title = form.title.data
        author = form.author.data
        year_of_publication = form.year_of_publication.data
        about = form.about.data

        if title:
            book_for_change.title = title
        if year_of_publication:
            book_for_change.year_of_publication = year_of_publication
        if author:
            book_for_change.author = author
        if about:
            book_for_change.about = about
        db.session.commit()


def book_exchange_request_func(book_id, current_user):
    new_exchange = Exchange(
        user_id=Book.query.get(book_id).owner,
        book_id=book_id,
        requester_id=current_user.id,
        status='pending'
    )
    db.session.add(new_exchange)
    db.session.commit()


def book_accept_request_func(exchange_id):
    accept_request = Exchange.query.get(exchange_id)

    # Change
    book_for_give = Book.query.get(accept_request.book_id)
    book_for_give.user_id = accept_request.requester_id

    accept_request.status = 'accepted'
    accept_request.accepted_date = datetime.today()

    db.session.commit()


def book_give_back_func(book_id):
    book_give_back = Book.query.get(book_id)
    book_give_back.user_id = book_give_back.owner

    end_of_exchange = Exchange.query.filter_by(book_id=book_id)
    end_of_exchange = end_of_exchange.order_by(Exchange.created_date.desc()).first()

    end_of_exchange.status = 'done'
    end_of_exchange.return_date = datetime.today()

    db.session.commit()


def book_delete_func(book_id):
    book_for_delete = Book.query.get(book_id)
    db.session.delete(book_for_delete)
    db.session.commit()
