from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

change_book_info = Blueprint('change_book_info', __name__)


@change_book_info.route('/change_book_info/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def book_change_info(book_page_id):
    # Search book for change info in Books
    book_for_change = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        book_for_change.book = request.form['book']
        book_for_change.year_of_publication = request.form['year_of_publication']
        book_for_change.author = request.form['author']
        book_for_change.about = request.form['about']
        try:
            db.session.commit()
            return redirect(url_for('main.index'))
        except Warning:
            db.session.rollback()
            flash('!')
            return render_template('change_book_info.html', book_for_change=book_for_change)
    return render_template('change_book_info.html', book_for_change=book_for_change)
