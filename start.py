from app import create_app
from data import db_session


app = create_app()

if __name__ == '__main__':
    db_session.global_init("db/newsfeed.db")
    app.run(debug=True)
