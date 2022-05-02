from flask import Blueprint, render_template
from flask_login import login_required

from ..extensions import db
from ..models.user import User
from ..models.books import Books

admin_main = Blueprint('admin_main', __name__)


@admin_main.route('/admin_main', methods=['GET', 'POST'])
@login_required
def index_admin():
    all_users = db.session.query(User).all()
    books_res = db.session.query(Books).all()
    return render_template('admin_main.html', user_res=all_users, books_res=books_res)