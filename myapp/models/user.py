from extensions import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(50), nullable=True, unique=True)
    psw = db.Column(db.String(50), nullable=True)

    bk = db.relationship('Books', backref='users', uselist=False)

    def __repr__(self):
        return f'{self.email}'
