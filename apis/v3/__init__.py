from flask import Blueprint
from flask_restx import Api, fields

bp = Blueprint('v3', __name__)
api = Api(bp)

resp_model = api.model('Response', {
    'msg': fields.String(default='Success')
})

publisher_model = api.model('Publisher', {
    'id': fields.Integer,
    'title': fields.String
})

genre_model = api.model('Genre', {
    'id': fields.Integer,
    'name': fields.String
})

user_state_model = api.model('UserState', {
    'liked': fields.Boolean
})

book_model = api.model('Book', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'publisher': fields.Nested(publisher_model),
    'price': fields.Integer,
    'published_at': fields.DateTime,
    'genres': fields.Nested(genre_model),
    'like_count': fields.Integer,
    'user_state': fields.Nested(user_state_model, skip_none=True)
})

user_model = api.model('User',{
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String,
    'role': fields.Integer
})

user_response = api.inherit('UserResponse', resp_model, {
    'user': fields.Nested(user_model)
})


from .books import ns as books_ns
from .publisher import ns as publisher_ns
from .genres import ns as genre_ns
from .users import ns as user_ns
from .auth import ns as auth_ns

api.add_namespace(books_ns, path='/books')
api.add_namespace(publisher_ns, path='/publishers')
api.add_namespace(genre_ns, path='/genres')
api.add_namespace(user_ns, path='/users')
api.add_namespace(auth_ns, path='/auth')