from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='El nombre de usuario es requerido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='La contraseña es requerida')])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message='El nombre de usuario es requerido')])
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido')
    ])
    password = PasswordField('Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        EqualTo('password2', message='Las contraseñas deben coincidir')
    ])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(message='Debes confirmar tu contraseña')])
    submit = SubmitField('Registrarse')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Por favor usa un nombre de usuario diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Por favor usa un email diferente.')

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='El email es requerido'),
        Email(message='Ingresa un email válido')
    ])
    submit = SubmitField('Solicitar Restablecimiento')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva Contraseña', validators=[
        DataRequired(message='La contraseña es requerida'),
        EqualTo('password2', message='Las contraseñas deben coincidir')
    ])
    password2 = PasswordField('Repetir Contraseña', validators=[DataRequired(message='Debes confirmar tu contraseña')])
    submit = SubmitField('Restablecer Contraseña')