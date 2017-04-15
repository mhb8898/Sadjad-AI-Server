#!/usr/bin/env python
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from model.map import Map
app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret!'

socketio = SocketIO(app)



game=dict()


#website

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/<id_game>')
def game_view(id_game):
    return render_template('game.html',token=id_game)

#client

@socketio.on('connect', namespace='/game')
def connect_client():
    pass
@socketio.on('init', namespace='/game')
def init_game(token):
    print token,"client",type(token)
    game[token]=Map()
    emit('result', {'token':token,'data': game[token].to_json()})

@socketio.on('touch', namespace='/game')
def touch(token,i,j):
    # print i,j
    game[token].touch(i,j)
    emit('result', {'data': game[token].to_json()},room=token)
    emit('result', {'data': game[token].to_json()})

@socketio.on('disconnect', namespace='/game')
def disconnect():
    pass
#viewer

@socketio.on('auth',namespace='/game')
def auth_viewer(data):
    print rooms()
    token=data['token']
    print token,"viewer",type(token)
    if token not in game:
        game[token]=Map()
    join_room(token)
    emit('result', {'token':token,'data': game[token].to_json()})

if __name__ == '__main__':
    socketio.run(app, debug=True)
