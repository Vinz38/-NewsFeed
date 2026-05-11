from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TelField, EmailField
from wtforms.fields.simple import BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    midlename = StringField('Midlename', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')