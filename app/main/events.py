from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from .models import storeMessage


@socketio.on('joined', namespace='/chat')
def joined(message):
    room = session.get('room')
    join_room(room)
    msg = '<' + session.get('name') + ' has entered the room.' + '>'
    emit('status', {'msg': msg}, room=room)
    storeMessage(msg, room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = session.get('room')
    msg = session.get('name') + ':' + message['msg']
    emit('message', {'msg': msg}, room=room)
    storeMessage(msg, room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = session.get('room')
    leave_room(room)
    msg = '<' + session.get('name') + ' has left the room.' + '>'
    emit('status', {'msg': msg}, room=room)
    storeMessage(msg, room)
