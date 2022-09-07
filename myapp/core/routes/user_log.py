from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from myapp.core.models.user import User
from myapp.core.forms.user_forms import LoginFrom


user_log = Blueprint('log', __name__)


@user_log.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFrom()
    if form.validate_on_submit():
        login_email = form.email.data
        whose_login = User.query.filter_by(email=login_email).first()
        if whose_login and check_password_hash(whose_login.psw, form.psw.data):
            login_user(whose_login)
            return redirect(url_for('main.index'))
        else:
            flash("User not found")
            return render_template('login.html')
    return render_template('login.html', form=form)


@user_log.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))
