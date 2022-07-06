from models import db

class Genre(db.Model):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)

    @classmethod
    def find_in(cls, ids):
        if len(ids) == 0:
            return []
        return cls.query.filter(cls.id.in_(ids)).all()