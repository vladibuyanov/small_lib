from myapp import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(260), nullable=True, unique=True)
    psw = db.Column(db.String(50), nullable=True)
    place = db.Column(db.String(32), nullable=True)
    user_photo = db.Column(db.String(50), default='default.png')

    books = db.relationship('Book', backref='user', uselist=True)

    def __init__(self, name, email, psw, place):
        self.name = name
        self.email = email
        self.psw = psw
        self.place = place

    def __repr__(self):
        return f'User {self.email}'
