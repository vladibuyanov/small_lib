from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.security import check_password_hash

from ..extensions import db
from ..models.user import User
from ..models.books import Books

logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['GET', 'POST'])
@login_required
def logo():
    logout_user()
    return redirect(url_for('main.index'))
