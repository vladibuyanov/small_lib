from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash

from extensions import db
from models.user import User


user_registration = Blueprint('user_registration', __name__)


@user_registration.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        # User with this email not exist
        user = {'name': request.form['name'], 'email': request.form['email'],
                'psw': request.form['psw'], 'psw_2': request.form['psw_2']}
        if not User.query.filter_by(email=user['email']).first():
            # Password not empty
            if user['psw'] and user['psw_2']:
                # 1-st and 2-nd input password the same
                if user['psw'] and user['psw_2']:
                    user['psw'] = generate_password_hash(user['psw'], method='sha256')
                    try:
                        new_user = User(name=user['name'], email=user['email'], psw=user['psw'])
                        db.session.add(new_user)
                        db.session.flush()
                        db.session.commit()
                    # Problem with add new user
                    except Warning:
                        db.session.rollback()
                        flash("Something's  going wrong. Please, try again")
                        return render_template('registration.html')
                    return redirect(url_for('log.user_login'))
                # 1-st and 2-nd input password not same
                else:
                    flash('Incorrect password. Please, try again')
                    return render_template('registration.html')
            # Password is empty
            else:
                flash('Empty password. Please, try again')
                return render_template('registration.html')
        # User already exist
        else:
            flash('User with this email already exist')
            return render_template('registration.html')
    else:
        return render_template('registration.html')
