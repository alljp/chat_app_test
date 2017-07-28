from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .models import storeMessage


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    msg = '< {} has entered the room. >'.format(session.get('name'))
    emit('status', {'msg': msg,
                    'user': session.get('name')}, room=room)
    storeMessage(msg, session.get('name'), room, "Status")


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    # msg = '{}: {}' .format(session.get('name'), message['msg'])
    emit('message', {'msg': message['msg'],
                     'user': session.get('name')}, room=room)
    storeMessage(message['msg'], session.get('name'), room, "Text")


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    msg = '< {} has left the room. >'.format(session.get('name'))
    emit('status', {'msg': msg,
                    'user': session.get('name')}, room=room)
    storeMessage(msg, session.get('name'), room, "Status")


@socketio.on('image', namespace='/chat')
def image(message):
    room = session.get('room')
    msg = '<img src = "{}">'.format(message['msg'])
    emit('image', {'msg': message['msg'],
                   'user': session.get('name')}, room=room)
    storeMessage(message['msg'], session.get('name'), room, "Image")
