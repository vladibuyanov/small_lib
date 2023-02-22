from datetime import datetime

from myapp import db, Book, Exchange


def book_add_func(request, current_user):
    add_new_book = Book(
        title=request.form['book'],
        author=request.form['author'],
        about=request.form['about'],
        year_of_publication=request.form['year_of_publication'],
        owner=current_user.id
    )
    db.session.add(add_new_book)
    db.session.commit()


def book_change_info_func(request, book_page_id):
    book_for_change = Book.query.filter_by(id=book_page_id).first()
    if request.method == 'GET':
        return book_for_change
    else:
        if request.form['title']:
            book_for_change.title = request.form['title']
        if request.form['year_of_publication']:
            book_for_change.year_of_publication = request.form['year_of_publication']
        if request.form['author']:
            book_for_change.author = request.form['author']
        if request.form['about']:
            book_for_change.about = request.form['about']
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
