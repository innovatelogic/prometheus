from flask import render_template
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_socketio import emit

from flask_babel import Babel, gettext, lazy_gettext
from flask_babel import _
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from app import app

#----------------------------------------------------------------------------------------------
@app.route('/')
@app.route("/index")
@mobile_template("{_mobile/}index.html")
def index(template):
    return render_template(template, title='Home', **locals())

#----------------------------------------------------------------------------------------------
@app.route("/about")
@mobile_template("{_mobile/}about.html")
def about(template):
    pass

#----------------------------------------------------------------------------------------------
@app.route("/legal")
@mobile_template("{_mobile/}legal.html")
def legal(template):
   pass

#----------------------------------------------------------------------------------------------
@app.route("/contacts")
@mobile_template("{_mobile/}contacts.html")
def contacts(template):
    pass