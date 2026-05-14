from flask_wtf import FlaskForm
from wtforms import StringField, TelField, EmailField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Optional


class EditProfileForm(FlaskForm):
    user_name = StringField('User Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone_number = TelField('Phone Number', validators=[DataRequired()])
    categories = SelectMultipleField('Сategory', validators=[Optional()], coerce=int)
    submit = SubmitField('Изменить профиль')
