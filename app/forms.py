from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, TextAreaField, TelField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Đăng nhập')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    phone_number = TelField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    year = IntegerField('Year', validators=[DataRequired()])
    role = SelectField('Role', choices=['Người kêu gọi/Tình nguyện viên', 'Nhà hảo tâm'], validators=[DataRequired()])
    work_place = StringField('Work place', validators=[DataRequired()])
    description = TextAreaField('Description')
    submit = SubmitField('Đăng ký')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

    def validate_phone_number(self, phone_number):
        user = User.query.filter_by(email=phone_number.data).first()
        if user is not None:
            raise ValidationError('Please use a different phone number.')