from email.policy import default

from flask_restful import Resource, reqparse, abort
from data import db_session
from data.categories import Category
from data.user import User
import flask

update_parser = reqparse.RequestParser()
update_parser.add_argument('user_name', required=True,
                           help="Username cannot be blank!")
update_parser.add_argument('email', required=True,
                           help="Email cannot be blank!")
update_parser.add_argument(
    'phone_number', help="Phone number cannot be blank!")
update_parser.add_argument('categories', type=list,
                           location='json', default=[])

parser = reqparse.RequestParser()
parser.add_argument('user_name', required=True,
                    help="Username cannot be blank!")
parser.add_argument('email', required=True, help="Email cannot be blank!")
parser.add_argument('hashed_password', required=True,
                    help="Password cannot be blank!")
parser.add_argument('phone_number', help="Phone number cannot be blank!")
parser.add_argument('categories', required=False,
                    type=list, location='json', default=[])

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', required=True,
                          help="Email cannot be blank!")
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
        return {'success': 'OK'}

    def get(self, user_id):
        abort_if_user_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user_data = user.to_dict(
            only=('user_name', 'email', 'phonenumber', 'categories'),
            rules=('-categories.users', '-categories.user')
        )
        user_data['phone_number'] = user_data.pop(
            'phonenumber', user.phone_number)
        return {'user': user_data}

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = update_parser.parse_args()   # ← здесь новый парсер
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        user.user_name = args['user_name']
        user.email = args['email']
        if args['phone_number']:
            user.phone_number = args['phone_number']
        categories = args.get('categories', [])
        if categories:
            user.categories = session.query(Category).filter(
                Category.id.in_(categories)).all()
        session.commit()
        return {'success': 'OK'}


class UserListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        user_list = []
        for item in users:
            user_item = item.to_dict(
                only=('user_name', 'email', 'phonenumber', 'categories'))
            user_item['phone_number'] = user_item.pop(
                'phonenumber', item.phone_number)
            user_list.append(user_item)
        return {'users': user_list}

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        if session.query(User).filter(User.email == args['email']).first():
            return flask.jsonify({'error': 'Email already exists'}), 400
        user = User(
            user_name=args['user_name'],
            email=args['email'],
            phone_number=args['phone_number'],
        )
        user.set_password(args['hashed_password'])
        session.add(user)
        categories = args.get('categories', [])
        if categories:
            user.categories = session.query(Category).filter(
                Category.id.in_(categories)).all()
        session.commit()

        return {'success': 'OK', 'user_id': user.id}


class UserLoginResource(Resource):
    def post(self):
        args = login_parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).filter(User.email == args['email']).first()
        if not user or not user.check_password(args['hashed_password']):
            return {'error': 'Invalid email or password'}, 401

        user_data = user.to_dict(
            only=('id', 'user_name', 'email', 'phonenumber', 'categories.name'))
        user_data['phone_number'] = user_data.pop(
            'phonenumber', user.phone_number)
        return {'user': user_data}
