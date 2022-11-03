from enum import Enum
from functools import wraps

import bcrypt
from flask_jwt_extended import get_jwt

from models import User as MUser


class Access():
    @classmethod
    def check_uniq_email(cls, argsemail):
        user = cls.get_user_by_email(argsemail)
        return user is None

    @classmethod
    def check_log_pass(cls, argsemail, argspassword):
        user = cls.get_user_by_email(argsemail)
        if user:
            passwd_hash = user.password_hash
            return bcrypt.checkpw(argspassword.encode('utf-8'), passwd_hash)
        return False

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
        user = MUser.query.get(userid)
        if user:
            if user.role > 1:
                return True
        return False


class Role(Enum):
    user = 1
    moderator = 2
    admin = 3


def jwt_guard(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            jwt = get_jwt()
            role = Role(jwt['role'])
            if role not in allowed_roles:
                return {'msg': 'Not allowed'}, 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

