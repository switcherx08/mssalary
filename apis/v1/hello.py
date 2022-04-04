from flask_restx import Resource, Namespace

ns = Namespace('hello')
books = {}
counter = 1

@ns.route('/')
class Hello(Resource):
    def get(self):
        return list(books.values())


    def post(self):
        global counter
        title = 'abc'
        book = {'id': counter,
                'title': title
                }
        books[counter] = book
        counter += 1
        return book
