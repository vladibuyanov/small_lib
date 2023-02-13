from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from myapp import Book, db, User

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
            year_of_publication=request.form['year_of_publication'],
            about=request.form['about'],
            owner=current_user.id,
            user_id=current_user.id
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


@books.route(f'{base_url}/give/<int:book_page_id>', methods=methods)
@login_required
def give(book_page_id):
    template = f'{template_folder}/give.html'

    if request.method == 'GET':
        return render_template(template)
    else:
        book_for_give = Book.query.filter_by(id=book_page_id).first()
        email_to_give = request.form['give_book_to_email']
        user_to_give = User.query.filter_by(email=email_to_give).first()
        book_for_give.user_id = user_to_give.id
        try:
            db.session.commit()
            return redirect(url_for('users.page', user_id=current_user.id))
        except Warning:
            db.session.rollback()
            return render_template(template)


@books.route(f'{base_url}/give_back/<int:book_page_id>')
@login_required
def give_back(book_page_id):
    book_for_give_back = Book.query.filter_by(id=book_page_id).first()
    book_for_give_back.user_id = current_user.id
    try:
        db.session.commit()
        flash('Ok')
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
