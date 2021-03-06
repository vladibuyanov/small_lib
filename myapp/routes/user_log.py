from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash

from models.user import User


user_log = Blueprint('log', __name__)


# Login page
@user_log.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login_email = request.form['login_email']
        whose_login = User.query.filter_by(email=login_email).first()
        # User exist
        if whose_login:
            login_psw = request.form['login_psw']
            # Correct password
            if check_password_hash(whose_login.psw, login_psw):
                login_user(whose_login)
                return redirect(url_for('main.index'))
            # Incorrect password
            else:
                flash('Incorrect password')
                return render_template('login.html')
        # User not exist
        else:
            flash("User not found")
            return render_template('login.html')
    else:
        return render_template('login.html')


@user_log.route('/logout', methods=['GET', 'POST'])
@login_required
def user_logout():
    logout_user()
    return redirect(url_for('main.index'))
