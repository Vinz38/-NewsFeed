from flask_restful import Resource, reqparse, abort
from data import db_session
from data.news import News
import flask


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


parser = reqparse.RequestParser()
parser.add_argument('link_news', required=True, help="Link cannot be blank!")
parser.add_argument('users', required=True, help="Users cannot be blank!")
parser.add_argument('categories', required=True,
                    help="Categories cannot be blank!")


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return news.to_dict(
            only=('id', 'link_news', 'users', 'categories'))

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return flask.jsonify({'success': 'OK'})

    def put(self, news_id):
        args = parser.parse_args()
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        if news:
            news.link_news = args['link_news']
            news.users = args['users']
            news.categories = args['categories']
        else:
            news = News(
                id=news_id,
                link_news=args['link_news'],
                users=args['users'],
                categories=args['categories']
            )
            session.add(news)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return flask.jsonify({'news': [item.to_dict(
            only=('id', 'link_news', 'users', 'categories')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            link_news=args['link_news'],
            users=args['users'],
            categories=args['categories']
        )
        session.add(news)
        session.commit()
        return flask.jsonify({'success': 'OK'})
