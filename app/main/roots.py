import flask
from data import db_session
from flask import jsonify, make_response, request, render_template

main_blueprint = flask.Blueprint(
    'roots_api',
    __name__,
    template_folder='templates'
)

@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    return render_template('index.html')