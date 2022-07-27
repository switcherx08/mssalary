import bcrypt

from config import ApplicationConfig

from . import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    name = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.BINARY(60), nullable=False)
    role = db.Column(db.Integer, default=1) #1 = user , 2 = moderator, 3=admin

    @classmethod
    def check_uniq_email(cls, argsmail):
        check_email = cls.query.filter_by(email=argsmail).first()
        if check_email is None:
            return True
        return False

    @classmethod
    def check_log_pass(cls, argsemail, argspassword):
        email = cls.query.filter_by(email=argsemail).first()
        if email:
            passwd_hash = email.password_hash
        return bcrypt.checkpw(argspassword.encode('utf-8'), passwd_hash)

    @classmethod
    def get_passwd_hash(cls, argspassword):
        salt = bcrypt.gensalt()
        encoded_password = argspassword.encode('utf-8')
        return bcrypt.hashpw(encoded_password, salt)



