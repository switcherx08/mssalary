from . import db

book_genres = db.Table(
    'book_genres',
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('books.id'), primary_key=True)
)
