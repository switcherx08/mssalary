from flask import Flask
from apis import bp as api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api') #регистрирую путь к версиям Api


if __name__ == '__main__':
    app.run(use_reloader=True)








