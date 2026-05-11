from flask import Blueprint
from flask_restful import Api
from .news_flaskrestful_MODEL import NewsListResource, NewsResource

news_api_blueprint = Blueprint('news_api', __name__)
news_api = Api(news_api_blueprint)
news_api.add_resource(NewsResource, '/api/news/<int:news_id>')
news_api.add_resource(NewsListResource, '/api/news/<string:category>')
