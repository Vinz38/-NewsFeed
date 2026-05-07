from datetime import timedelta

from data import db_session
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_restful_MODELS.news_flaskrestful_MODEL import NewsResource, NewsListResource


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADER_NAME'] = "authorization"
jwt = JWTManager(app)

api.add_resource(NewsResource, '/api/news/<int:news_id>')
api.add_resource(NewsListResource, '/api/news/<list:category>')

db_session.global_init("db/newsfeed.db")
db_sess = db_session.create_session()
