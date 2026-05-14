from flask import Blueprint
from flask_restful import Api

from .categories_flaskrestful_MODEL import CategoryListResource
from .news_flaskrestful_MODEL import NewsListResource, NewsResource
from .users_flaskrestful_MODEL import UserResource, UserListResource, UserLoginResource, UserCategoryResource

api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)
api.add_resource(NewsResource, '/api/news/<int:news_id>')
api.add_resource(NewsListResource, '/api/news/<string:category>')
api.add_resource(UserResource, '/api/users/<int:user_id>')
api.add_resource(UserCategoryResource, '/api/user/category/<int:user_id>')
api.add_resource(UserListResource, '/api/users')
api.add_resource(UserLoginResource, '/api/login')
api.add_resource(CategoryListResource, '/api/categories')
