from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user
from werkzeug.security import generate_password_hash

from myapp import db
from myapp.core.models.user import User
from myapp.core.forms.user_forms import RegisterForm

user_registration = Blueprint('user_registration', __name__)


@user_registration.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegisterForm()
    new_user = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if not new_user:
            form.psw = generate_password_hash(form.psw.data, method='sha256')
            add_new_user = User(form.name.data, form.email.data, form.psw, place=None)

            db.session.add(add_new_user)
            db.session.flush()
            db.session.commit()

            login_user(add_new_user)
            return redirect(url_for('main.index'))
        else:
            flash('User with this email already exist')
            return render_template('registration.html')
    return render_template('registration.html', form=form)

