from flask import session, redirect, url_for, render_template, request, flash
from passlib.hash import sha256_crypt
from . import main
from . import forms
from . import models


@main.route('/', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    error = session.get('error')
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
        error = models.registerUser(name, password)
        if error:
            return render_template('register.html', error=error)
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
    error = 'Not logged in!'
    return render_template('login.html', form=forms.LoginForm, error=error)


@main.route('/chat/<room>/', methods=['GET', 'POST'])
def chat(room):
    form = forms.ChatForm()
    if session.get('name'):
        if request.form.get('remove'):
            remove(room)
        if request.form.get('add'):
            add(room)
        admin = session.get('name') == models.getAdmin(room)
        users = models.roomsUsers(room) if admin else None
        allusers = models.retrieveUsers() if admin else None
        rooms = models.usersRooms(session['name'])
        if room in rooms:
            history = models.retrieveHistory(room)
            return render_template('chat.html', name=session.get('name'),
                                   room=room, history=history, form=form,
                                   rooms=rooms, admin=admin, users=users,
                                   allusers=allusers)
        else:
            session['error'] = 'Not a member of the room - {}'.format(room)
            return redirect(url_for('.index'))
    session['error'] = 'You are not logged in!'
    return redirect(url_for('.login'))


def remove(room):
    print("Remove")
    users = request.form.getlist('users')
    print(users)
    for user in users:
        print(user)
        models.leaveRoom(user, room)
    models.removeUsers(room, users)
    return redirect(url_for('.chat', room=room))


def add(room):
    users = request.form.getlist('users')
    for user in users:
        models.joinRoom(user, room)
    models.addUsers(room, users)
    return redirect(url_for('.chat', room=room))


@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('.login'))


@main.route('/create-room/', methods=['GET', 'POST'])
def create_room():
    if session.get('name'):
        if request.method == 'POST':
            room = request.form.get('room')
            users = request.form.getlist('users')
            for user in users:
                models.joinRoom(user, room)
            models.createRoom(room, session['name'])
            models.addUsers(room, users)
            return ("<p>Room-{} created</p>".format(room))

        else:
            users = models.retrieveUsers()
            return render_template('create_room.html', users=users)
    return redirect(url_for('.login'))
