from flask import Blueprint, render_template, request, url_for, flash, redirect, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


# Admin page
@admin.route('/main', methods=["POST", "GET"])
def main():
    info = 'info'
    print(session.get('admin_logged'))
    return render_template('admin/main.html', info=info)


# Login page
@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        admin_user = request.form['admin_user']
        admin_psw = request.form['admin_psw']
        if admin_user == 'admin' and admin_psw == 'admin':
            login_admin()
            return redirect(url_for('.main'))
        else:
            flash("Something's  going wrong. Please, try again")
            return render_template('admin/login.html')
    return render_template('admin/login.html')


# Logout
@admin.route('/logout', methods=['GET', 'POST'])
def logout():
    if isLogged():
        logout_admin()
        return redirect(url_for('.login'))
    return redirect(url_for('.login'))
