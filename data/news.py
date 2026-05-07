import sqlalchemy
from . db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from datetime import timedelta

class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "news"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    categories = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    link_news = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    live_time = sqlalchemy.Column(sqlalchemy.DateTime, default=timedelta(days=7))