from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, logout_user
from werkzeug.security import generate_password_hash

from myapp import Books, db, User

users = Blueprint('users', __name__)


@users.route('/user/<int:user_id>')
def page(user_id):
    all_user_dp = db.session.query(User).all()
    user_books = Books.query.filter_by(owner=user_id).all()

    took_book = []
    all_user_books = Books.query.filter_by(user_id=user_id).all()
    for book in all_user_books:
        if book.user_id == user_id and user_id != book.owner:
            took_book.append(book)

    return render_template('user/user_page.html',
                           user_res=all_user_dp[user_id - 1],
                           users=all_user_dp,
                           user_books=user_books,
                           took_book=took_book,
                           number_of_took_book=len(took_book)
                           )


@users.route('/user/user_settings/<int:user_id>', methods=['GET', 'POST'])
@login_required
def settings(user_id):
    if current_user.id == user_id:
        user_settings = User.query.filter_by(id=user_id).first()
        if request.method == "POST":
            if request.form['settings_name']:
                user_settings.name = request.form['settings_name']
            if request.form['settings_email']:
                user_settings.email = request.form['settings_email']
            if request.form['settings_password']:
                user_settings.password = generate_password_hash(
                    request.form['settings_password'],
                    method='sha256'
                )
            if request.form['settings_place']:
                user_settings.place = request.form['settings_place']
            try:
                db.session.commit()
                return redirect(url_for('users.page', user_id=user_id))
            except Warning:
                db.session.rolback()
                flash('Something going wrong')
                return redirect(url_for('main.index'))
        return render_template('user/user_settings.html', user_settings=user_settings)
    else:
        return redirect(url_for('main.index'))


@users.route('/user/user_settings/delete/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete(user_id):
    logout_user()
    delete_user = User.query.filter_by(id=user_id).first()
    try:
        db.session.delete(delete_user)
        db.session.commit()
        return redirect(url_for('main.index'))
    except Warning:
        db.session.rollback()
        return redirect(url_for('main.index'))
