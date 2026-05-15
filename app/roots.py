from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import (
    verify_jwt_in_request, get_jwt_identity, unset_jwt_cookies
)
import flask
import requests
from flask import request, render_template, redirect, flash
import schedule_script
from .forms.edit_profile_form import EditProfileForm
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
    news = []
    try:
        verify_jwt_in_request(optional=True)
        user_id = get_jwt_identity()
        if user_id:
            resp = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}')
            if resp.status_code == 200:
                if "application/json" in resp.headers.get("Content-Type", ""):
                    user = resp.json().get('user')
                    news = schedule_script.get_text_and_links(user_id)
                else:
                    print("API returned non-json response")
    except Exception as e:
        print("JWT ERROR:", e)

    return render_template(
        'main_page.html',
        user=user,
        title="NEWS",
        news=news
    )


@main_blueprint.route('/news_page')
def news_page():
    verify_jwt_in_request()
    user_id = get_jwt_identity()
    resp = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}')

    if resp.status_code == 200:
        if "application/json" in resp.headers.get("Content-Type", ""):
            user = resp.json().get('user')
        else:
            print("API returned non-json response")
    else:
        user = None
    link = request.args.get('link')
    if not link:
        return redirect('/')
    title = schedule_script.get_news(link, "title")
    text = schedule_script.get_news(link, "text")
    return render_template('news_page.html', title=title, text=text, user=user)


@main_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        response_api = requests.post('http://127.0.0.1:5000/api/login', json={
            'email': form.email.data,
            'hashed_password': form.password.data
        })

        if response_api.status_code != 200:
            error_msg = "Произошла ошибка на сервере"
            if response_api.status_code == 401:
                error_msg = "Неверный логин или пароль"

            return render_template(
                'login.html',
                message=error_msg,
                form=form
            )

        user = response_api.json().get("user")

        access_token = create_access_token(identity=str(user['id']))

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
            'user_name': form.user_name.data,
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


@main_blueprint.route('/profile')
def profile():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()

        resp = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}')

        if resp.status_code == 200:
            if "application/json" in resp.headers.get("Content-Type", ""):
                user = resp.json().get('user')
            else:
                print("API returned non-json response")
        else:
            user = None

    except Exception as e:
        print("JWT ERROR:", e)
        user = None

    return render_template(
        'profile.html',
        user=user,
        title="Профиль"
    )


@main_blueprint.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    verify_jwt_in_request()
    user_id = get_jwt_identity()

    resp_api = requests.get(f'http://127.0.0.1:5000/api/users/{user_id}')

    if resp_api.status_code == 200:
        if "application/json" in resp_api.headers.get("Content-Type", ""):
            user_data = resp_api.json().get('user')
        else:
            print("API returned non-json response")
    else:
        user_data = None
    from types import SimpleNamespace
    user_obj = SimpleNamespace(**user_data)
    form = EditProfileForm(obj=user_obj)
    cat_all = [(k['id'], k['name']) for k in
               requests.get('http://127.0.0.1:5000/api/categories').json().get('categories', [])]
    form.categories.choices = cat_all

    if form.validate_on_submit():
        if form.categories.data:
            cat_user = form.categories.data
        updated_data = {
            'user_name': form.user_name.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'categories': cat_user
        }
        resp = requests.put(
            f'http://127.0.0.1:5000/api/users/{user_id}', json=updated_data)
        if resp.status_code == 200:
            if "application/json" in resp.headers.get("Content-Type", ""):
                flash('Профиль успешно обновлен', 'success')
                return redirect('/profile')
            else:
                print("API returned non-json response")
        else:
            flash('Ошибка при обновлении профиля', 'danger')

    return render_template(
        'edit_profile.html', form=form, title="Редактирование профиля", user=user_data)


@main_blueprint.route('/logout')
def logout():
    response = redirect('/')
    unset_jwt_cookies(response)
    return response
