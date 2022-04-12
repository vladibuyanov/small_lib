from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

from admin.admin import admin

# Configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = 'd6c25d2b8081e4df4f6c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///small-lib_2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.register_blueprint(admin, url_prefix='/admin')


db = SQLAlchemy(app)
login_manager = LoginManager(app)


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
    about = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# Variables
books_res = db.session.query(Books).all()
user_res = db.session.query(User).all()
# all_res = db.session.query(User, Books).join(Books, User.id == Books.user_id).all()


# Main page
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', user_res=user_res, books_res=books_res)


# Users dynamic page
@app.route('/<int:page_id>')
def user(page_id):
    return render_template('page_id.html', user_res=user_res[page_id - 1], books_res=books_res)


# Add book page
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        try:
            book_from_page = Books(
                book=request.form['book'],
                author=request.form['author'],
                about=request.form['about'],
                user_id=current_user.id
            )
            db.session.add(book_from_page)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Something is going wrong')
        return redirect(url_for('index'))
    else:
        return render_template('add.html')


# Registration page
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.form['psw'] == request.form['psw_2']:
            try:
                user_from_page = User(
                    name=request.form['name'],
                    email=request.form['email'],
                    psw=request.form['psw']
                )
                db.session.add(user_from_page)
                db.session.flush()
                db.session.commit()
            except:
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
        filter_email = User.query.filter_by(email=request.form['login_email']).all()
        if len(filter_email) > 0:
            if request.form['login_psw'] == filter_email[0].psw:
                login_user(filter_email[0])
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
