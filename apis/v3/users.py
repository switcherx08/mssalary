from flask_restx import Resource, Namespace, reqparse, fields
from apis.v3 import resp_model, user_response, user_model
from models import User as MUser


ns = Namespace('users')


user_list_response = ns.inherit('UserListResponse', resp_model, {
    'users': fields.List(fields.Nested(user_model))
})

user_get_parser = reqparse.RequestParser()
user_get_parser.add_argument('user_id', type=int, location='args')
# user_get_parser.add_argument('email', type=str)
# user_get_parser.add_argument('name', type=str)
# user_get_parser.add_argument('password_hash', type=str)

@ns.route('/<int:id>')
class User(Resource):
    @ns.marshal_with(user_response, skip_none=True)
    def get(self, id):
        args = user_get_parser.parse_args()
        user = MUser.query.get(id)
        return {'user': user}
    def post(self):
        pass

