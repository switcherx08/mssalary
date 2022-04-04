from flask import Blueprint
from flask_restx import Api
from .hello import ns as hello_ns

bp = Blueprint('v1', __name__)
api = Api(bp)

api.add_namespace(hello_ns, path='/hello')

