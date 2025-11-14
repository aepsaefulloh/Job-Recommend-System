"""
Forms for Job Recommendation System
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from models import User

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    """Registration form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired()])
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Administrator')],
                       default='user', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class SurveyFilterForm(FlaskForm):
    """Form for filtering survey data in dashboard"""
    status_bekerja = SelectField('Status Bekerja',
                                choices=[('', 'All'), ('Ya', 'Sudah Bekerja'), ('Tidak', 'Belum Bekerja')])
    jurusan = SelectField('Jurusan', choices=[('', 'All')])
    tempat_tinggal = SelectField('Tempat Tinggal', choices=[('', 'All')])
    jenis_perusahaan = SelectField('Jenis Perusahaan', choices=[('', 'All')])
    submit = SubmitField('Filter')