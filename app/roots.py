from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies
import flask
import requests
from flask import jsonify, make_response, request, render_template, redirect, flash
from data import db_session
from data.user import User
from .forms.register_form import RegisterForm
from flask_jwt_extended import create_access_token
from .forms.login_form import LoginForm


main_blueprint = flask.Blueprint(
    'roots_api',
    __name__,
    template_folder='templates'
)


@main_blueprint.route('/')
@main_blueprint.route('/index')
def index():
    user = None

    try:
        verify_jwt_in_request(optional=True)

        user_id = get_jwt_identity()

        if user_id:
            db_sess = db_session.create_session()
            user = db_sess.query(User).get(user_id)

    except Exception as e:
        print("JWT ERROR:", e)

    return render_template(
        'index.html',
        user=user,
        title="NEWS"
    )


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(
            User.email == form.email.data
        ).first()

        if not user or not user.check_password(form.password.data):
            return render_template(
                'login.html',
                message="Неверный логин или пароль",
                form=form
            )

        access_token = create_access_token(identity=str(user.id))

        response = redirect('/')

        set_access_cookies(response, access_token)

        return response

    return render_template(
        'login.html',
        title='Авторизация',
        form=form
    )


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
            flash(
                f'Ошибка: {resp.json().get("error", "Неизвестная ошибка")}', 'danger')
    return render_template('register.html', title='Регистрация', form=form)


@main_blueprint.route('/logout')
def logout():
    response = redirect('/')

    unset_jwt_cookies(response)

    return response
