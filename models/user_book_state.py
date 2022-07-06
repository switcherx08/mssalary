from models import db


class UserBookState(db.Model):
    __tablename__ = 'user_book_states'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    liked = db.Column(db.Boolean, default=False)
    user = db.relationship('User', uselist=False)

