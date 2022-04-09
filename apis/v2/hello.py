from flask_restx import Resource, Namespace

ns = Namespace('books')
books_dict = {}
counter = 1
request_book = 5

# Переписать код генерации книг через генератор питона
def books_generate1():
    books_dict = {}


# Реализовать генератор словаря books, чтобы приложение стартовало сразу с 5 книгами
def books_generate():
    global counter
    for books in range(6):
        title = 'Kniga'
        description = 'is good'
        book = {
            'id': counter,
            'title': title + str(counter),
            'description': title + ' ' + description,
        }
        books_dict[counter] = book
        counter += 1
#    return f'Книг добавлено: {counter}' #Понять, как вернуть результат функции в консоль во время работы сервера.

books_generate()

# Реализовать filter, который из словаря books будет возвращать только книги с указанным title
@ns.route('/')
class Books(Resource):
    def get(self):
        knigi = list(books_dict.values())
        if len(knigi) <= request_book:
            return 'Такой книги точно нет, там:' + str(knigi)
        else:
            return knigi[request_book -1]

#title будет записывать в объект book еще и description
    def post(self):
        global counter
        title = 'Kniga'
        description = 'is good'
        book = {
            'id': counter,
            'title': title + str(counter),
            'description': title + ' ' + description,
        }
        books_dict[counter] = book
        counter += 1
        return f'Добавлено значение: {book}'












