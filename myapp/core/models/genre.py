from myapp import db


class Genre(db.Model):
    __tablename__ = 'genre'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)

    books = db.relationship('Book', backref='genre', uselist=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return str(self.name)
