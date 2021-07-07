import os
from flask import Flask, render_template, request, redirect, url_for, session,g
from flask_socketio import SocketIO, join_room, leave_room, emit

application = Flask(__name__)
application.secret_key = "Neelesh_0609"
socketio = SocketIO(application)

application = Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')

@application.route('/game', methods=['GET', 'POST'])
def game():
    if request.method == 'POST':
        usertype = request.form.get('user')
        username = request.form.get('username')
        room = request.form.get('room')
        print(usertype)
        print(username)
        print(room)
        session.pop('user', None)
        session['user'] = username
        session['room'] = room
        session['usertype'] = usertype

        if usertype == 'player1':
            return render_template('game.html', username=username, room=room, category=usertype, legend = "Player 1")
        elif usertype == 'player2':
            return render_template('game.html', username=username, room=room, category=usertype, legend = "Player 2")
        else:
            return render_template('index.html')

    return render_template('index.html')


@application.before_request
def before_request():
    g.user = None
    if 'user' in session:
       g.user = session['user']


@socketio.on('join', namespace='/game')
def join(message):
    room = message['room']
    join_room(room)
    usertype = session['usertype']
    emit('status', {'msg': usertype + " " + message['username'] + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/game')
def text(message):
    room = message['room']
    usertype = session['usertype']
    emit('message', {'msg': usertype + " " + message['username'] + ' : ' + message['msg']}, room=room)


@application.route("/logout")
def logout():
    session.pop('user', None)
    session.pop('room', None)
    return render_template('index.html')


@application.route("/endgame")
def endgame():
    session.pop('user', None)
    return render_template('index.html')


if __name__=="__main__":
    application.run()
