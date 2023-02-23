from flask_login import logout_user, login_user
from werkzeug.security import generate_password_hash, check_password_hash

from myapp.core.forms.auth_forms import RegisterForm, LoginFrom
from myapp.core.models.user import User, db


def registration_func(request):
    form = RegisterForm()

    if request.method == 'GET':
        return form

    if User.query.filter_by(email=form.email.data).first():
        return False

    if form.validate_on_submit():
        form.psw = generate_password_hash(form.psw.data, method='sha256')
        add_new_user = User(
            name=form.name.data,
            email=form.email.data,
            psw=form.psw,
            place=None
        )
        db.session.add(add_new_user)
        db.session.commit()
        login_user(add_new_user)
        return True


def user_login_func(request):
    form = LoginFrom()

    if request.method == 'GET':
        return form

    user_login = User.query.filter_by(email=form.email.data).first()

    if not user_login:
        return False

    if form.validate_on_submit():
        if user_login and check_password_hash(user_login.psw, form.psw.data):
            login_user(user_login)
            return True


def user_logout_func():
    logout_user()
