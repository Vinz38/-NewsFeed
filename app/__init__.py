from datetime import timedelta
import requests
from flask import Flask
from app.roots import main_blueprint
from data import db_session
from data.user import User
from .api.init_api import api_blueprint
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'f8d2c4a9b7e1f3d6c8a0b2e4f6d8a1c3'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token"
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    jwt = JWTManager(app)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    return app
