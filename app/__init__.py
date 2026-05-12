from datetime import timedelta
import requests
from flask import Flask
from app.roots import main_blueprint
from data import db_session
from data.user import User
from .api.init_api import api_blueprint
from flask_jwt_extended import JWTManager
from flask_login import login_user, current_user, LoginManager, logout_user, login_required

login_manager = LoginManager()


def create_app():
    app = Flask(__name__, template_folder='../templates')
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['JWT_IDENTITY_CLAIM'] = 'user'
    app.config['JWT_HEADER_NAME'] = "authorization"
    jwt = JWTManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db_sess = db_session.create_session()
        return db_sess.query(User).get(int(user_id))

    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    return app
