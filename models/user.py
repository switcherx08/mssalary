from config import ApplicationConfig
from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Integer, default=1) #1 = user , 2 = moderator, 3=admin

    @classmethod
    def check_uniq_email(cls, argsmail):
        find_email = cls.query.filter_by(email=argsmail).first()
        if find_email is None:
            return True
        return False



