from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

# Not used
# from flask_migrate import Migrate
# migrate = Migrate(app, db)

# blueprint
# from flask import blueprint
# from admin.admin import admin
# app.register_blueprint(admin, url_prefix='/admin')

# Variables
# all_res = db.session.query(User, Books).join(Books, User.id == Books.user_id).all()
# user_res = db.session.query(User).all()
# books_res = db.session.query(Books).all()

from config import *

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# For login
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# database
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    psw = db.Column(db.String(50), nullable=True)

    bk = db.relationship('Books', backref='users', uselist=False)

    def __repr__(self):
        return self.email


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(20))
    year_of_publication = db.Column(db.String(5))
    about = db.Column(db.String)
    owner = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# Main page
@app.route('/', methods=['GET', 'POST'])
def index():
    # Take all users
    all_users = db.session.query(User).all()
    # Take all books
    books_res = db.session.query(Books).all()
    return render_template('index.html', user_res=all_users, books_res=books_res)


# Users dynamic page
@app.route('/<int:page_id>')
def user(page_id):
    # Take all user for dynamic page
    all_user_dp = db.session.query(User).all()
    # All books of user from page
    user_books = Books.query.filter_by(owner=all_user_dp[page_id - 1].id).all()
    return render_template('page_id.html',
                           user_res=all_user_dp[page_id - 1],
                           user_books=user_books,
                           users=all_user_dp)


# Add book page
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            book_from_page = Books(
                book=request.form['book'],
                author=request.form['author'],
                year_of_publication=request.form['year_of_publication'],
                about=request.form['about'],
                owner=current_user.id,
                user_id=current_user.id
            )
            db.session.add(book_from_page)
            db.session.commit()
        except Warning:
            db.session.rollback()
            flash('Something is going wrong')
        return redirect(url_for('index'))
    else:
        return render_template('add.html')


# Change book info
@app.route('/change_book_info/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def change_book_info(book_page_id):
    # Search book for change info in Books
    book_for_change = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        book_for_change.book = request.form['book']
        book_for_change.year_of_publication = request.form['year_of_publication']
        book_for_change.author = request.form['author']
        book_for_change.about = request.form['about']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Warning:
            db.session.rollback()
            return redirect(url_for('index'))
    return render_template('change_book_info.html', book_for_change=book_for_change)


# Give book
@app.route('/give_book/<int:book_page_id>', methods=['GET', 'POST'])
@login_required
def give_book(book_page_id):
    # Search book for giving in Books
    book_for_give = Books.query.filter_by(id=book_page_id).first()
    if request.method == 'POST':
        # Give book to 'user_to_give'
        email_to_give = request.form['give_book_to_email']
        user_to_give = User.query.filter_by(email=email_to_give).first()
        book_for_give.user_id = user_to_give.id
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Warning:
            db.session.rollback()
            return redirect(url_for('index'))
    return render_template('give_book.html')


# Delete book
@app.route('/del/<int:book_page_id>')
@login_required
def delete_book(book_page_id):
    # Search book for delete
    book_for_delete = Books.query.filter_by(id=book_page_id).first()
    try:
        db.session.delete(book_for_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Warning:
        db.session.rollback()
        return redirect(url_for('index'))


# Registration page
@app.route('/registration', methods=['GET', 'POST'])
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
                return redirect(url_for('index'))
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


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form['login_email']
        whose_login = User.query.filter_by(email=login_email).first()
        # User exist
        if whose_login:
            login_psw = request.form['login_psw']
            # Correct password
            if check_password_hash(whose_login.psw, login_psw):
                login_user(whose_login)
                return redirect(url_for('index'))
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


# Logout
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
