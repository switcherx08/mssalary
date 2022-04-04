from flask import Blueprint
from .v1 import bp as api_v1
from .v2 import bp as api_v2


bp = Blueprint('api', __name__) #объект блюпринта
bp.register_blueprint(api_v1, url_prefix='/v1') #регистрация пути к 1 версии
bp.register_blueprint(api_v2, url_prefix='/v2') #регистрация пути к 2 верси