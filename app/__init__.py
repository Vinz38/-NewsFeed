from datetime import timedelta

from flask import Flask
from .main.roots import main_blueprint
from .api import news_api_blueprint
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['JWT_IDENTITY_CLAIM'] = 'user'
    app.config['JWT_HEADER_NAME'] = "authorization"
    jwt = JWTManager(app)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(news_api_blueprint)
    return app
