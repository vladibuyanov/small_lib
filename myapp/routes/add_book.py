from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

add_book = Blueprint('add_book', __name__)


# Add book page
@add_book.route('/add', methods=['GET', 'POST'])
@login_required
def book_add():
    if request.method == 'POST':
        try:
            book_from_page = Books(
                book=request.form['book'],
                author=request.form['author'],
                year_of_publication=request.form['year_of_publication'],
                about=request.form['about'],
                owner=current_user.id,
                user_id=current_user.id
            )
            db.session.add(book_from_page)
            db.session.commit()
        except Warning:
            db.session.rollback()
            flash('Something is going wrong')
        return redirect(url_for('index'))
    else:
        return render_template('add.html')
