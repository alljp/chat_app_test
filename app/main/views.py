from flask import session, redirect, url_for, render_template, request, flash
from passlib.hash import sha256_crypt
from . import main
from . import forms
from . import models


@main.route('/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    error = None
    if request.method == 'POST':
        name = form.name.data
        password = str(form.password.data)
        if not models.validateUser(name, password):
            error = 'Invalid Credentials.'
        else:
            session['name'] = name
            return redirect(url_for('.index'))
    return render_template('login.html', error=error)


@main.route('/register/', methods=['GET', 'POST'])
def register():
    form = forms.RegistrationForm()
    if request.method == 'POST':
        print("Success")
        name = form.name.data
        password = sha256_crypt.encrypt((str(form.password.data)))
        models.registerUser(name, password)
        # session['logged_in'] = True
        session['name'] = name
        return redirect(url_for('.index'))
    return render_template('register.html')


@main.route('/chat/', methods=['GET', 'POST'])
def index():
    form = forms.ChatForm()
    allrooms = models.retrieveRooms()
    if session.get('name'):
        rooms = models.usersRooms(session['name'])
        if request.method == 'POST':
            room = session['room'] = form.room.data
            return redirect(url_for('.chat', room=room))
        if request.method == 'GET':
            form.room.data = ''
            return render_template('index.html', form=form, allrooms=allrooms,
                                   rooms=rooms, error=session.get('error'))
    return render_template('login.html', form=forms.LoginForm)


@main.route('/chat/<room>/', methods=['GET', 'POST'])
def chat(room):
    form = forms.ChatForm()
    name = session.get('name', '')
    room = room
    rooms = models.usersRooms(name)
    if request.method == 'POST':
        if name == '':
            return redirect(url_for('.login'))
        if room == '':
            return redirect(url_for('.index'))
        return render_template('chat.html', name=name, room=room,
                               history=history, form=form, rooms=rooms)
    if name and room in rooms:
        history = models.retrieveHistory(room)
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
