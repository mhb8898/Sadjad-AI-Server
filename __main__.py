#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from model.map import Map
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)



game=dict()
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/game')
def connect():
    token = 1
    game[token]=Map()
    emit('result', {'token':token,'data': game[token].to_json()})

@socketio.on('touch', namespace='/game')
def touch(token,i,j):
    game[token].touch(i,j)
    emit('result', {'data': game[token].to_json()})


if __name__ == '__main__':
    socketio.run(app, debug=True)
