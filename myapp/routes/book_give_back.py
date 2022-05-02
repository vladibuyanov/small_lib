from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from ..extensions import db
from ..models.user import User
from ..models.books import Books

book_give_back = Blueprint('book_give_back', __name__)


@book_give_back.route('/book_give_back/<int:book_page_id>')
@login_required
def book_gb(book_page_id):
    # Search book for giving in Books
    book_for_give_back = Books.query.filter_by(id=book_page_id).first()
    book_for_give_back.user_id = current_user.id
    try:
        db.session.commit()
        return redirect(url_for('main.index'))
    except Warning:
        db.session.rollback()
        flash('!')
        return render_template(url_for('main.index'))
