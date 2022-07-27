from flask import Flask
from flask_jwt_extended import JWTManager

from apis import bp as api_bp
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)


db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')  # регистрирую путь к версиям Api


@app.before_first_request
def init_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(use_reloader=True)

# import flask_jwt_extended
#
