import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime, timedelta


def default_live_time():
    return datetime.now() + timedelta(days=7)


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "news"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    categories = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link_news = sqlalchemy.Column(sqlalchemy.String, nullable=False, unique=True)
    live_time = sqlalchemy.Column(sqlalchemy.DateTime, default=default_live_time)
    dob = sqlalchemy.Column(sqlalchemy.DateTime, default=sqlalchemy.func.now())
