from flask import Blueprint, render_template
from flask_login import login_required

from ..extensions import db
from ..models.user import User
from ..models.books import Books

user_settings = Blueprint('user_settings', __name__)


@user_settings.route('/user_settings/<int:user_id>')
@login_required
def settings(user_id):
    return render_template('user_settings.html')
