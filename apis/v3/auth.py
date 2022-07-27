from flask_restx import Resource, Namespace, reqparse, fields, marshal_with
import bcrypt

from models import User as MUser, db

from apis.v3 import user_response

ns = Namespace('auth')

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', required=True)
signup_parser.add_argument('password', required=True)
signup_parser.add_argument('name', required=True)


login_parser = reqparse.RequestParser()
login_parser.add_argument('Authorization', required=True, location='headers')

@ns.route('/signup')
class Signup(Resource):
    @marshal_with(user_response, skip_none=True)
    def post(self):
        args = signup_parser.parse_args()
        salt = bcrypt.gensalt()
        encoded_password = args.password.encode('utf-8')
        password_hash = bcrypt.hashpw(encoded_password, salt)
        if not MUser.check_uniq_email(args.email):
            return {'msg': 'User with E-Mail that you entered already exist'}
        user = MUser(email=args.email, name=args.name, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return {'user': user}




@ns.route('/login')
class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        auth = args.Authorization
        return auth