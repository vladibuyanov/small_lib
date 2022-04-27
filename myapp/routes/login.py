from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash

from ..extensions import db
from ..models.user import User
from ..models.books import Books

login = Blueprint('login', __name__)


# Login page
@login.route('/login', methods=['GET', 'POST'])
def logi():
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
