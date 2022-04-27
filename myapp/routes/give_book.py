from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

give_book = Blueprint('give_book', __name__)


@give_book.route('/give_book/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def book_give(book_page_id):
    # Search book for giving in Books
    book_for_give = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        # Give book to 'user_to_give'
        email_to_give = request.form['give_book_to_email']
        user_to_give = User.query.filter_by(email=email_to_give).first()
        book_for_give.user_id = user_to_give.id
        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except Warning:
            db.session.rollback()
            flash('!')
            return render_template('give_book.html')
    return render_template('give_book.html')
