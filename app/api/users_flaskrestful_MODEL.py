from email.policy import default

from flask_restful import Resource, reqparse, abort
from data import db_session
from data.categories import Category
from data.user import User
from flask_jwt_extended import create_access_token
import flask

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True, help="Surname cannot be blank!")
parser.add_argument('name', required=True, help="Name cannot be blank!")
parser.add_argument('midlename', required=True,
                    help="Midlename cannot be blank!")
parser.add_argument('email', required=True, help="Email cannot be blank!")
parser.add_argument('hashed_password', required=True,
                    help="Password cannot be blank!")
parser.add_argument('phone_number', help="Phone number cannot be blank!")
parser.add_argument('categories', required=False, type=list, location='json', default=[])

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True, help="Email cannot be blank!")
login_parser.add_argument('hashed_password', required=True,
                          help="Password cannot be blank!")


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(user_id)
    if not user:
        abort(404, message=f"User {user_id} not found")


class UserResource(Resource):
    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return flask.jsonify({'success': 'OK'})

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user_data = user.to_dict(
            only=('surname', 'name', 'midlename', 'email', 'phonenumber'))
        user_data['phone_number'] = user_data.pop('phonenumber', user.phone_number)
        return flask.jsonify({'user': user_data})


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        user_list = []
        for item in users:
            user_item = item.to_dict(only=('surname', 'name', 'midlename', 'email', 'phonenumber'))
            user_item['phone_number'] = user_item.pop('phonenumber', item.phone_number)
            user_list.append(user_item)
        return flask.jsonify({'users': user_list})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).first():
            return flask.jsonify({'error': 'Email already exists'}), 400
        user = User(
            surname=args['surname'],
            name=args['name'],
            midlename=args['midlename'],
            email=args['email'],
            phone_number=args['phone_number'],
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        categories = args.get('categories', [])
        if categories:
            user.categories = session.query(Category).filter(Category.id.in_(categories)).all()
        session.commit()

        access_token = create_access_token(identity=user.id)
        return flask.jsonify({'success': 'OK', 'user_id': user.id})


class UserLoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args['email']).first()
        if not user or not user.check_password(args['hashed_password']):
            return flask.jsonify({'error': 'Invalid email or password'}), 401
    
        return flask.jsonify({'sucsess': 'OK', 'user_id': user.id})

class UserCategoryResource(Resource):
    def get(self, user_id):
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        category_list = [k.name for k in user.categories]
        return flask.jsonify({'category': category_list})