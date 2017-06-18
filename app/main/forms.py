from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms import validators


class LoginForm(FlaskForm):
    name = StringField('Name', [validators.Required()])
    password = PasswordField('Password', [validators.Required()])
    submit = SubmitField('Login')


class ChatForm(FlaskForm):
    room = StringField('Room', [validators.Required()])
    submit = SubmitField('Enter Chatroom')
