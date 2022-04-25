from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

from config import secret_key

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///small-lib.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# database
db = SQLAlchemy(app)
# migrate = Migrate(app, db)

login_manager = LoginManager(app)

# blueprint
# from admin.admin import admin
# app.register_blueprint(admin, url_prefix='/admin')


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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Variables
# all_res = db.session.query(User, Books).join(Books, User.id == Books.user_id).all()
# user_res = db.session.query(User).all()
# books_res = db.session.query(Books).all()


# Main page
@app.route('/', methods=['GET', 'POST'])
def index():
    user_res = db.session.query(User).all()
    books_res = db.session.query(Books).all()
    return render_template('index.html', user_res=user_res, books_res=books_res)


# Users dynamic page
@app.route('/<int:page_id>')
def user(page_id):
    # list of users books
    user_res = db.session.query(User).all()
    user_books = Books.query.filter_by(owner=user_res[page_id - 1].id).all()
    return render_template('page_id.html', user_res=user_res[page_id - 1], user_books=user_books, users=user_res)


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
    book_for_change = Books.query.filter_by(id=book_page_id).all()[0]
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
    book_for_give = Books.query.filter_by(id=book_page_id).all()[0]
    if request.method == 'POST':
        email_to_give = request.form['give_book_to_email']
        book_for_give.user_id = User.query.filter_by(email=email_to_give).all()[0].id
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
    book_for_delete = Books.query.filter_by(id=book_page_id).all()[0]
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
        if request.form['psw'] == request.form['psw_2']:
            name = request.form['name']
            email = request.form['email']
            psw = generate_password_hash(request.form['psw'], method='sha256')
            try:
                new_user = User(name=name, email=email, psw=psw)
                db.session.add(new_user)
                db.session.flush()
                db.session.commit()
            except Warning:
                db.session.rollback()
                flash("Something's  going wrong. Please, try again")
                return render_template('registration.html')
            return redirect(url_for('index'))
        else:
            flash('Incorrect password. Please, try again')
            return render_template('registration.html')
    else:
        return render_template('registration.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_email = request.form['login_email']
        login_psw = request.form['login_psw']
        whose_login = User.query.filter_by(email=login_email).all()[0]
        if whose_login:
            if check_password_hash(whose_login.psw, login_psw):
                login_user(whose_login)
                return redirect(url_for('index'))
            else:
                flash('Incorrect password')
                return render_template('login.html')
        else:
            flash("User's not found")
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