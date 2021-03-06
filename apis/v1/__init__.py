from flask import Blueprint
from flask_restx import Api
from .books import ns as books_ns

bp = Blueprint('v1', __name__)
api = Api(bp)

api.add_namespace(books_ns, path='/books')

