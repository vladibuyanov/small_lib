from flask import Blueprint, redirect, url_for
from flask_login import login_required, logout_user


logout = Blueprint('logout', __name__)


@logout.route('/logout', methods=['GET', 'POST'])
@login_required
def logo():
    logout_user()
    return redirect(url_for('main.index'))
