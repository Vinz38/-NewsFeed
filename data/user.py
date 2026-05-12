from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


liu_table = sqlalchemy.Table(
    'liu',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('news', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('news.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class User(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "users"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    midlename = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    email = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    phonenumber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    @property
    def phone_number(self):
        return self.phonenumber

    @phone_number.setter
    def phone_number(self, value):
        self.phonenumber = value

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)