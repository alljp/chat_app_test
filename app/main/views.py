from flask import session, redirect, url_for, render_template, request, flash
from passlib.hash import sha256_crypt
from . import main
from .forms import LoginForm, ChatForm
from .models import *


@main.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if request.method == 'POST':
        name = form.name.data
        password = str(form.password.data)
        print("\n\n\n", name+" "+password)
        if not validateUser(name, password):
            error = 'Invalid Credentials.'
        else:
            session['name'] = name
            return redirect(url_for('.index'))
    return render_template('login.html', error=error)


@main.route('/chat', methods=['GET', 'POST'])
def index():
    form = ChatForm()
    if session.get('name'):
        print(session['name'])
        if request.method == 'POST':
            session['room'] = form.room.data
            return redirect(url_for('.chat', room=session['room']))
        if request.method == 'GET':
            form.room.data = ''
            return render_template('index.html', form=form)
    return render_template('login.html', form=LoginForm)


@main.route('/chat/<room>')
def chat(room):
    name = session.get('name', '')
    room = room
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, room=room)
