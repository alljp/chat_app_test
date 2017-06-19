from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SelectField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    name = StringField('Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Login')


class ChatForm(FlaskForm):
    room = SelectField('Room', [validators.Required()], id='room')
    submit = SubmitField('Enter Chatroom')


class RegistrationForm(FlaskForm):
    name = StringField('Name', [validators.Required()])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
