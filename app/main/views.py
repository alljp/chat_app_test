from flask import session, redirect, url_for, render_template, request, flash
from passlib.hash import sha256_crypt
from . import main
from .forms import LoginForm, ChatForm, RegistrationForm
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


@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        print("Success")
        name = form.name.data
        print("\n\n", form.name.data, form.password.data)
        print(form)
        password = sha256_crypt.encrypt((str(form.password.data)))
        registerUser(name, password)
        # session['logged_in'] = True
        session['name'] = name
        return redirect(url_for('.index'))
    return render_template('register.html')


@main.route('/chat', methods=['GET', 'POST'])
def index():
    form = ChatForm()
    if session.get('name'):
        print(session['name'])
        rooms = usersRooms(session['name'])
        if request.method == 'POST':
            room = session['room'] = form.room.data
            return redirect(url_for('.chat', room=room))
        if request.method == 'GET':
            form.room.data = ''
            return render_template('index.html', form=form,
                                   rooms=rooms, error=session.get('error'))
    return render_template('login.html', form=LoginForm)


@main.route('/chat/<room>', methods=['GET', 'POST'])
def chat(room):
    form = ChatForm()
    name = session.get('name', '')
    room = room
    if request.method == 'POST':
        if name == '':
            return redirect(url_for('.login'))
        if room == '':
            return redirect(url_for('.index'))
        rooms = usersRooms(name)
        return render_template('chat.html', name=name, room=room,
                               history=history, form=form, rooms=rooms)
    rooms = usersRooms(name)
    if name and room in rooms:
        history = retrieveHistory(room)
        return render_template('chat.html', history=history,
                               form=form, rooms=rooms)
    else:
        session['error'] = "Not a member of the room - {}".format(room)
        return redirect(url_for('.index'))
    return redirect(url_for('.login'))


@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('.login'))
