from flask_restful import Resource, reqparse, abort
from data import db_session
from data.news import News
import flask


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, message=f"News {news_id} not found")


def not_unique_news(link):
    session = db_session.create_session()
    news = session.query(News).filter(News.link_news == link).all()
    if news:
        abort(404, message=f"Base already have this news")


parser = reqparse.RequestParser()
parser.add_argument('link_news', required=True, help="Link cannot be blank!")
parser.add_argument('categories', required=True,
                    help="Categories cannot be blank!")
parser.add_argument('live_time', help="Live time cannot be blank!")


class NewsResource(Resource):
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
            news.categories = args['categories']
            news.live_time = args['live_time']
        else:
            news = News(
                id=news_id,
                link_news=args['link_news'],
                categories=args['categories'],
                live_time=args['live_time']
            )
            session.add(news)
        session.commit()
        return flask.jsonify({'success': 'OK'})


class NewsListResource(Resource):
    def get(self, category):
        session = db_session.create_session()
        news = session.query(News).all()
        if category:
            category = category.split(',')
        if news.categories in category:
            return flask.jsonify({'news': [item.to_dict(
                only=('link_news', 'categories', 'live_time')) for item in news]})
        return flask.jsonify({'news': []})

    def post(self, category):
        args = parser.parse_args()
        not_unique_news(args['link_news'])
        session = db_session.create_session()
        news = News(
            link_news=args['link_news'],
            categories=args['categories'],
            live_time=args['live_time']
        )
        session.add(news)
        session.commit()
        return flask.jsonify({'success': 'OK'})
