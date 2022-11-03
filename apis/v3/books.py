from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from flask_restx import Resource, Namespace, reqparse, fields

from apis.parsers import list_parser
from apis.v3 import resp_model, book_model
from apis.v3.access import Access, jwt_guard, Role
from models import Book as MBook, db, Genre as MGenre, UserBookState as MUserBookState, User as MUser

ns = Namespace('books')

book_response = ns.inherit('BookResponse', resp_model, {
    'book': fields.Nested(book_model, skip_none=True),
})

book_list_response = ns.inherit('BookListResponse', resp_model, {
    'books': fields.List(fields.Nested(book_model)),
    'page_count': fields.Integer
})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('description', required=False, type=str)
parser.add_argument('publisher_id', required=True, type=int)
parser.add_argument('price', required=True, type=int)
parser.add_argument('published_at', required=False)
parser.add_argument('genres', required=False, action='append', type=int, default=[])

get_parser = reqparse.RequestParser()
get_parser.add_argument('title', required=False, type=str, location='args')
get_parser.add_argument('page', required=False, type=int, location='args', default=1)
get_parser.add_argument('by', required=False, type=str, location='args')
get_parser.add_argument('order', required=False, type=str, location='args')
get_parser.add_argument('limit', required=False, type=int, location='args', default=5)
get_parser.add_argument('publisher_id', required=False, type=int, location='args')
get_parser.add_argument('genres', required=False, type=list_parser(), default=[], location='args')
get_parser.add_argument('user_id', required=False, type=int, location='args')

like_parser = reqparse.RequestParser()
like_parser.add_argument('liked', required=True, type=bool)
#like_parser.add_argument('user_id', required=True, type=int)

temp_parser = reqparse.RequestParser()
temp_parser.add_argument('user_id', required=False, type=int, location='args')


@ns.route('/<int:id>')
class Book(Resource):
    @ns.marshal_with(book_response, skip_none=True)
    def get(self, id):
        args = temp_parser.parse_args()
        book = MBook.find(id, user_id=args.user_id)
        if book is None:
            return {'msg': 'not found'}, 404

        return {'book': book}

    @ns.marshal_with(book_response)
    def put(self, id):
        args = parser.parse_args()
        book = MBook.query.get(id)
        if book is None:
            return {'msg': 'not found'}, 404
        book.title = args.title
        book.description = args.description
        book.genres = MGenre.find_in(args.genres)
        db.session.commit()
        return {'book': book}

    @ns.marshal_with(book_response, skip_none=True)
    def delete(self, id):
        book = MBook.query.get(id)
        if book is None:
            return {'msg': f'could not delete, this book (id {id}) doesn\'t exist'}, 404
        print(book)
        db.session.delete(book)
        db.session.commit()
        return {'book': book}


@ns.route('/')
class BookList(Resource):
    @ns.marshal_list_with(book_list_response)
    def get(self):
        args = get_parser.parse_args()
        books = MBook.find_all(**args)
        page_count = MBook.count_pages(**args)

        return {'books': books, 'page_count': page_count}

    #Решение ПУНКТА 4 ДЗ
    #@jwt_guard(roles=[2,3])
    @jwt_required()
    @ns.marshal_with(book_response)
    @jwt_guard([Role.moderator, Role.admin])
    def post(self):
        args = parser.parse_args()
        args.genres = MGenre.find_in(args.genres)
        book = MBook(**args)  # MBook(title=args.title, description=args.description)
        book.published_at = datetime.now()  # .strftime('%Y-%m-%d-%H.%M.%S')
        db.session.add(book)
        db.session.commit()
        return {'book': book}


#решение пункта 3 ДЗ :
@ns.route('/<int:id>/like/')
class BookLikes(Resource):
    @jwt_required()
    @ns.marshal_with(book_response)
    def post(self, id):
        args = like_parser.parse_args()
        book = MBook.find(id, get_jwt_identity())
        if book is None:
            return {'msg': 'book not found'}, 404

        if book.user_state is None:
            book.user_state = MUserBookState(liked=False, user_id=get_jwt_identity(), book_id=id)

        if book.user_state.liked != args.liked:
            book.like_count = MBook.like_count + (1 if args.liked else -1)
            book.user_state.liked = args.liked

            db.session.commit()

        return {'book': book}


