from flask import Flask
from apis import bp as api_bp
from models import db

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

app.register_blueprint(api_bp, url_prefix='/api')  # регистрирую путь к версиям Api


@app.before_first_request
def init_tables():
    db.create_all()


if __name__ == '__main__':
    app.run(use_reloader=True)
