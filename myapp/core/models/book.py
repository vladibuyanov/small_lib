from myapp import db


class Book(db.Model):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=True)
    author = db.Column(db.String(20))
    year_of_publication = db.Column(db.String(5))
    about = db.Column(db.String)
    owner = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True, default=None)

    def __init__(self, title, author, year_of_publication, about, owner):
        self.title = title
        self.author = author
        self.year_of_publication = year_of_publication
        self.about = about
        self.owner = owner
        self.user_id = owner

    def __repr__(self):
        return self.title
