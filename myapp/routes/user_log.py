from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from models.user import User
from forms.user_forms import LoginFrom


user_log = Blueprint('log', __name__)


# Login page
@user_log.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginFrom()
    if form.validate_on_submit():
        login_email = form.email.data
        whose_login = User.query.filter_by(email=login_email).first()
        if whose_login:
            login_psw = form.psw.data
            if check_password_hash(whose_login.psw, login_psw):
                login_user(whose_login)
                return redirect(url_for('main.index'))
            else:
                flash('Incorrect password')
                return render_template('login.html')
        else:
            flash("User not found")
            return render_template('login.html')
    return render_template('login.html', form=form)


@user_log.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))
