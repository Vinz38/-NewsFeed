import flask
import requests
from data import db_session
from flask import jsonify, make_response, request, render_template, redirect
from .forms.login_form import LoginForm
from .forms.register_form import RegisterForm

main_blueprint = flask.Blueprint(
    'roots_api',
    __name__,
    template_folder='templates'
)


@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    return render_template('index.html', title="NEWS")


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/')
    return render_template('login.html', title='Авторизация', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        requests.post('http://127.0.0.1:5000/api/users', json={
            'surname': form.surname.data,
            'name': form.name.data,
            'midlename': form.midlename.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'categories' : form.categories.data
        })
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)
