import bcrypt
from models import User as MUser


class Access():
    @classmethod
    def check_uniq_email(cls, argsemail):
        email = cls.get_user_by_email(argsemail)
        if email is None:
            return True
        return False

    @classmethod
    def check_log_pass(cls, argsemail, argspassword):
        email = cls.get_user_by_email(argsemail)
        if email:
            passwd_hash = email.password_hash
        return bcrypt.checkpw(argspassword.encode('utf-8'), passwd_hash)

    @classmethod
    def get_passwd_hash(cls, argspassword):
        salt = bcrypt.gensalt()
        encoded_password = argspassword.encode('utf-8')
        return bcrypt.hashpw(encoded_password, salt)

    @classmethod
    def get_user_by_email(cls, argsemail):
        return MUser.query.filter_by(email=argsemail).first()

    @classmethod
    def check_edit_access(cls, userid):
        query = MUser.query.filter_by(id=userid).first()
        if query:
            if query.role > 1:
                return True
        return False
