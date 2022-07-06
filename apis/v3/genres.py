from flask_restx import Resource, Namespace, reqparse, fields

from apis.v3 import resp_model, genre_model
from models import Genre as MGen, db

ns = Namespace('genres')

genre_response = ns.inherit('GenreResponse', resp_model, {
    'genre': fields.Nested(genre_model, skip_none=True),
})

genre_list_response = ns.inherit('GenreListResponse', resp_model, {
    'genres': fields.List(fields.Nested(genre_model))
})

parser = reqparse.RequestParser()
parser.add_argument('name', required=True, type=str)

get_parser = reqparse.RequestParser()
get_parser.add_argument('name', required=False, type=str, location='args')


@ns.route('/')
class GenreList(Resource):
    @ns.marshal_list_with(genre_list_response)
    def get(self):
        args = get_parser.parse_args()
        genres = MGen.query.all()
        return {'genres': genres}

    @ns.marshal_with(genre_response)
    def post(self):
        args = parser.parse_args()
        genre = MGen(**args)
        db.session.add(genre)
        db.session.commit()
        return {'genre': genre}
