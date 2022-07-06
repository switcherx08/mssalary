from models import db

class Publisher(db.Model):
    __tablename__ = 'publishers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    books = db.relationship('Book', back_populates='publisher', lazy=True) #бъявить в Book связь (relationship) с Publisher-ом. Реализовать backref, чтобы из Publisher-а был доступен список книг, которые к нему относятся

