from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash

from ..extensions import db
from ..models.user import User
from ..models.books import Books

user_registration = Blueprint('user_registration', __name__)


@user_registration.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # User with this email not exist
        name = request.form['name']
        email = request.form['email']
        is_exist = User.query.filter_by(email=email).first()
        if not is_exist:
            # 1-st and 2-nd input password the same
            if request.form['psw'] == request.form['psw_2']:
                psw = generate_password_hash(request.form['psw'], method='sha256')
                try:
                    new_user = User(name=name, email=email, psw=psw)  # <- Don't know how do this right.
                    db.session.add(new_user)
                    db.session.flush()
                    db.session.commit()
                # Problem with add new user
                except Warning:
                    db.session.rollback()
                    flash("Something's  going wrong. Please, try again")
                    return render_template('registration.html')
                return redirect(url_for('main.index'))
            # 1-st and 2-nd input password not same
            else:
                flash('Incorrect password. Please, try again')
                return render_template('registration.html')
        # User already exist
        else:
            flash('User with this email already exist')
            return render_template('registration.html')
    else:
        return render_template('registration.html')
