import sqlalchemy
from . db_session import SqlAlchemyBase
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin


class News(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "news"

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True)
    users = orm.relationship("User",
                             secondary="liu",
                             backref='news')
    categories = orm.relationship("Category",
                                  secondary="association",
                                  backref="news")
    link_news = sqlalchemy.Column(sqlalchemy.String, nullable=False)
