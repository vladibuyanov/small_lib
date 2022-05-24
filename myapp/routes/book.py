from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

book = Blueprint('book', __name__)


@book.route('/book/add', methods=['GET', 'POST'])
@login_required
def book_add():
    if request.method == 'POST':
        book_from_page = Books(
            book=request.form['book'],
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
            return render_template('book/add.html')
    else:
        return render_template('book/add.html')


@book.route('/book/change_info/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def change_info(book_page_id):
    book_for_change = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        book_for_change.book = request.form['book']
        book_for_change.year_of_publication = request.form['year_of_publication']
        book_for_change.author = request.form['author']
        book_for_change.about = request.form['about']
        try:
            db.session.commit()
            return redirect(url_for('users.page', user_id=current_user.id))
        except Warning:
            db.session.rollback()
            flash('Something going wrong')
            return render_template('book/change_info.html', book_for_change=book_for_change)
    return render_template('book/change_info.html', book_for_change=book_for_change)


@book.route('/book/give/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def give(book_page_id):
    book_for_give = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        # Give book to 'user_to_give'
        email_to_give = request.form['give_book_to_email']
        user_to_give = User.query.filter_by(email=email_to_give).first()
        book_for_give.user_id = user_to_give.id
        try:
            db.session.commit()
            return redirect(url_for('users.page', user_id=current_user.id))
        except Warning:
            db.session.rollback()
            flash('Something going wrong')
            return render_template('book/give.html')
    return render_template('book/give.html')


@book.route('/book/give_back/<int:book_page_id>')
@login_required
def give_back(book_page_id):
    # Search book for giving in Books
    book_for_give_back = Books.query.filter_by(id=book_page_id).first()
    book_for_give_back.user_id = current_user.id
    try:
        db.session.commit()
        flash('Ok')
        return redirect(url_for('users.page', user_id=current_user.id))
    except Warning:
        db.session.rollback()
        flash('Something gong wrong')
        return redirect(url_for('users.page', user_id=current_user.id))


@book.route('/book/delete/<int:book_page_id>')
@login_required
def delete_book(book_page_id):
    book_for_delete = Books.query.filter_by(id=book_page_id).first()
    try:
        db.session.delete(book_for_delete)
        db.session.commit()
        return redirect(url_for('users.page', user_id=current_user.id))
    except Warning:
        db.session.rollback()
        return redirect(url_for('users.page', user_id=current_user.id))
