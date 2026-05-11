from flask_restful import Resource, reqparse, abort
from data import db_session
from data.categories import Category
import flask


parser = reqparse.RequestParser()
parser.add_argument('name', required=True, help="Name cannot be blank!")


class CategoryListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Category).all()
        return flask.jsonify({'categories': [item.to_dict(
            only=('name', 'id')) for item in categories]})

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True,
                            help="Name cannot be blank!")
        args = parser.parse_args()
        session = db_session.create_session()
        category = Category(
            name=args['name']
        )
        session.add(category)
        session.commit()
        return flask.jsonify({'success': 'OK'})