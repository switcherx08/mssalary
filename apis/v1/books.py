from flask_restx import Resource, Namespace, reqparse

ns = Namespace('books')
books = {}
counter = 1

parser = reqparse.RequestParser()
parser.add_argument('title', required=True, type=str)
parser.add_argument('description', required=False, type=str)

get_parser = reqparse.RequestParser()
get_parser.add_argument('title', required=False, type=str, location='args')

@ns.route('/<int:id>')
class Book(Resource):
    def get(self, id):
        if id in books:
            return books[id]
        return {'message': 'not found'}, 404

    def put(self, id):
        args = parser.parse_args()
        if id in books:
            book = books[id]
            book.update(**args)
            return book
        return {'message': 'not found'}, 404

    # Реализовать HTTP-метод DELETE
    def delete(self, id):
        if id in books:
            return books.pop(id)
        return {'message': 'could not delete'}, 404


# Добавить фильтр формата GET /api/v1/books/?title=<title> с помощью (подсказка: нужно использовать RequestParser())


@ns.route('/')
class BookList(Resource):
    def get(self):
        args = get_parser.parse_args()
        if args.title is not None:
            return [book for book in books.values() if book['title'] == args.title]
        return list(books.values())

    def post(self):
        global counter
        args = parser.parse_args()
        book = {'id': counter,
                **args
                }
        books[counter] = book
        counter += 1
        return book
