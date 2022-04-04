from flask import Blueprint
from flask_restx import Api
from .hello import ns as books_ns

bp = Blueprint('v2', __name__) #блюпринт апи 2 версии
api = Api(bp) #инициализация рест функций

api.add_namespace(books_ns, path='/books')
