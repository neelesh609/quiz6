import os
from flask import Flask, render_template, request, redirect, url_for, session,g
from flask_socketio import SocketIO, join_room, leave_room, emit


application=Flask(__name__)


@application.route('/')
def index():
    return render_template('index.html')


if __name__=="__main__":
    application.run()
