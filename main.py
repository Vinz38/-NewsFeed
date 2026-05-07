from datetime import timedelta

from data import db_session
from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_simple import JWTManager 


app = Flask(__name__)
app = Api(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
app.config['JWT_EXPIRES'] = timedelta(days=1)
app.config['JWT_IDENTITY_CLAIM'] = 'user'
app.config['JWT_HEADEAR_NAME'] = "authorization"
app.jwt = JWTManager(app)


db_session.global_init("db/newsfeed.db")
db_sess = db_session.create_session()

'''user = User()
user.surname = "Никулин"
user.name = "Илья"
user.midlename = "Алексеевич"
user.email = "ilia.nikulin09@gmail.com"
user.phonenumber = "+79273962292"
user.hashed_password = "123123"

user1 = User()
user1.surname = "Епишкин"
user1.name = "Кирилл"
user1.midlename = "Максимович"
user1.email = "kirillep@gmail.com"
user1.phonenumber = "-"
user1.hashed_password = "123123123123"


category1 = Category()
category1.name = "спорт"
category2 = Category()
category2.name = "творчество"

db_sess.add(user)
db_sess.add(user1)
db_sess.add(category1)
db_sess.add(category2)  
db_sess.commit()

news1 = News()
news1.users.append(user)
news1.users.append(user1)
news1.categories.append(category1)
news1.categories.append(category2)
news1.link_news = "xui"


db_sess.add(news1)
db_sess.commit()'''