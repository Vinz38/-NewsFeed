import flask
import requests
import json
from flask import jsonify, make_response, request, render_template, redirect, flash
from flask_login import login_user, current_user, login_required, logout_user
from data import db_session
from data.user import User
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
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@main_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    cat_all = [(k['id'], k['name']) for k in
               requests.get('http://127.0.0.1:5000/api/categories').json().get('categories', [])]
    form.categories.choices = cat_all
    cat_user = []
    if form.validate_on_submit():
        if form.categories.data:
            cat_user = form.categories.data
        resp = requests.post('http://127.0.0.1:5000/api/users', json={
            'surname': form.surname.data,
            'name': form.name.data,
            'midlename': form.midlename.data,
            'hashed_password': form.password.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'categories': cat_user
        })
        if resp.status_code in (200, 201):
            return redirect('/login')
        else:
            print(resp.status_code, resp.text)
            flash(f'Ошибка: {resp.json().get("error", "Неизвестная ошибка")}', 'danger')
    return render_template('register.html', title='Регистрация', form=form)


@main_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")
