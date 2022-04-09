from flask_restx import Resource, Namespace, reqparse, fields
from models import Book as MBook, db

ns = Namespace('books')
books = {}
counter = 1

book_model = ns.model('Book', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'message': fields.String
})

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('description', required=False, type=str)

get_parser = reqparse.RequestParser()
get_parser.add_argument('title', required=False, type=str, location='args')


@ns.route('/<int:id>')
class Book(Resource):
    @ns.marshal_with(book_model, skip_none=True)
    def get(self, id):
        book = MBook.query.get(id)
        if book is None:
            return {'message': 'not found'}, 404
        return book

    # Реализовать метод PUT / api / v3 / books / < int: id >
    @ns.marshal_with(book_model)
    def put(self, id):
        args = parser.parse_args()
        book = MBook.query.get(id)
        if book is None:
            query = MBook(id=id, title=args.title, description=args.description)
            db.session.add(query)
            db.session.commit()
            #return book  --- вот так почему-то отдает запись до обновления , поэтому:
            newbook = MBook.query.get(id)
            return newbook
        book.title = args.title
        book.description = args.description
        db.session.commit()
        return book

    # Реализовать метод DELETE /api/v3/books/<int:id>
    @ns.marshal_with(book_model)
    def delete(self, id):
        book = MBook.query.get(id)
        if book is None:
            return {'message': 'could not delete, this book is not exist'}, 404
        print(book)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'book has been deleted successfully'}


# Добавить фильтр формата GET /api/v1/books/?title=<title> с помощью (подсказка: нужно использовать RequestParser())


@ns.route('/')
class BookList(Resource):
    @ns.marshal_list_with(book_model)
    def get(self):
        args = get_parser.parse_args()
        books = MBook.query.all()
        return books

    @ns.marshal_with(book_model)
    def post(self):
        args = parser.parse_args()
        book = MBook(**args)  # MBook(title=args.title, description=args.description)
        db.session.add(book)
        db.session.commit()
        print(args)
        print(book)
        return book
