from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

delete_book = Blueprint('delete_book', __name__)


@delete_book.route('/del/<int:book_page_id>')
@login_required
def book_delete(book_page_id):
    # Search book for delete
    book_for_delete = Books.query.filter_by(id=book_page_id).first()
    try:
        db.session.delete(book_for_delete)
        db.session.commit()
        return redirect(url_for('main.index'))
    except Warning:
        db.session.rollback()
        return redirect(url_for('main.index'))
