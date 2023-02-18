from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from myapp import db
from myapp.core.models.user import User
from myapp.core.forms.user_forms import LoginFrom, RegisterForm

auth = Blueprint('auth', __name__)
methods = ['GET', 'POST']
template_folder = 'pages/auth'
redirect_url = 'main.index'


@auth.route('/registration', methods=methods)
def registration():
    template = f'{template_folder}/registration.html'

    if current_user.is_authenticated:
        return redirect(url_for(redirect_url))

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
            return redirect(url_for(redirect_url))
        else:
            flash('User with this email already exist')
            return render_template(template)
    return render_template(template, form=form)


@auth.route('/login', methods=methods)
def user_login():
    template = f'{template_folder}/login.html'
    form = LoginFrom()

    if current_user.is_authenticated:
        return redirect(url_for(redirect_url))

    if request.method == 'GET':
        return render_template(template, form=form)

    else:
        login_email = form.email.data
        login_email = User.query.filter_by(email=login_email).first()

        if login_email and check_password_hash(login_email.psw, form.psw.data):
            login_user(login_email)
            return redirect(url_for(redirect_url))
        else:
            flash("User not found")
            return render_template(template)


@auth.route('/logout', methods=methods)
@login_required
def user_logout():
    logout_user()
    return redirect(url_for(redirect_url))
