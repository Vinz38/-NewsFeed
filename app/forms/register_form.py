from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TelField, EmailField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from requests import get


class RegisterForm(FlaskForm):
    surname = StringField('Surname', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    midlename = StringField('Midlename', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired()])
    categories = SelectMultipleField('Сategory', validators=[DataRequired()], coerce=int)
    submit = SubmitField('Войти')