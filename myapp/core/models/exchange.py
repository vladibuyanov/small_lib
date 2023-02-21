from datetime import datetime
from myapp import db


class Exchange(db.Model):
    __tablename__ = 'exchange'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'Exchange {self.id} from {self.user_id} to {self.requester_id}'
