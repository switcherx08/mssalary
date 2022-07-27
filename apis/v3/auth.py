from flask_jwt_extended import create_access_token
from flask_restx import Resource, Namespace, reqparse, fields, marshal_with
import bcrypt

from models import User as MUser, db

from apis.v3 import user_response, login_response

ns = Namespace('auth')

signup_parser = reqparse.RequestParser()
signup_parser.add_argument('email', required=True)
signup_parser.add_argument('password', required=True)
signup_parser.add_argument('name', required=True)


login_parser = reqparse.RequestParser()
#login_parser.add_argument('Authorization', required=True, location='headers')
login_parser.add_argument('email', required=True)
login_parser.add_argument('password', required=True)

@ns.route('/signup')
class Signup(Resource):
    @marshal_with(user_response, skip_none=True)
    def post(self):
        args = signup_parser.parse_args()
        if not MUser.check_uniq_email(args.email):
            return {'msg': 'User E-Mail that you entered already exists'}
        user = MUser(email=args.email, name=args.name, password_hash=MUser.get_passwd_hash(args.password))
        db.session.add(user)
        db.session.commit()
        return {'user': user}

@ns.route('/login')
class Login(Resource):
    @marshal_with(login_response, skip_none=True)
    def post(self):
        args = login_parser.parse_args()
        if MUser.check_log_pass(args.email, args.password):
            access_token = create_access_token(identity=args.email)
            return {'msg': True, 'access_token': access_token}
        return {'msg': 'Invalid Credentials'}