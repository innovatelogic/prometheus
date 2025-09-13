import os
import sys
import signal
import json
import uuid
from enum import Enum

from pprint import pprint

# Import flask module
from flask import Flask, session, request
from flask_login import LoginManager
from flask_socketio import SocketIO, emit
from flask_socketio import emit
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
from flask_cors import CORS
from flask_babel import Babel, gettext
from flask_mobility import Mobility
from flask_mobility.decorators import mobile_template
from jinja2 import Environment
import logging
from logging.handlers import RotatingFileHandler

import app.config.settings 

os.environ["OMP_NUM_THREADS"] = "1"

_app_locale = None

print("Init Flask App")
app = Flask(__name__, static_folder="static")
app.logger.setLevel(logging.INFO)

app_data_path = os.getenv('PROMETHEUS_APP_DATA', '/tmp')  # Default to '/tmp' if the variable is not set

# Construct the log file path
log_file_path = os.path.join(app_data_path, 'logs', 'app.log')

log_dir = os.path.dirname(log_file_path)
os.makedirs(log_dir, exist_ok=True)

if 'flask' in sys.argv[0]:
    app.config["DEBUG"] = True
    app.config["ENV"] = "development"

    io = SocketIO(app, cors_allowed_origins="*")
    logging.info("SocketIO initialized for Flask with CORS allowed.")
elif 'gunicorn' in sys.argv[0]:
    io = SocketIO(app, async_mode='gevent', cors_allowed_origins="*")

    # Configure logging with rotation
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    log_handler = RotatingFileHandler(
        log_file_path, maxBytes=100 * 1024 * 1024, backupCount=5  # 10 MB max size, keep 5 backups
    )
    log_handler.setFormatter(log_formatter)
    log_handler.doRollover()

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)

    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(message)s',
                        handlers=[log_handler])
    #logging.getLogger('werkzeug').setLevel(logging.ERROR)

    logging.info("SocketIO initialized for Gunicorn with gevent and CORS allowed.")
else:
    io = SocketIO(app)
    logging.info(f"SocketIO initialized with threading mode.")

babel_ = None
clients = {}

@io.on('connect')
def events_connect(auth):
    '''generate uuid on connection and send it back to client '''
    userid = str(uuid.uuid4())
    session['userid'] = userid
    clients[userid] = request.sid

    print("[events_connect] userid[token]= " + str(userid))
    print("[events_connect] request.sid=" + str(request.sid))
    print("[events_connect] current_user.is_authenticated=" + str(current_user.is_authenticated))

    if current_user.is_authenticated:
        print("[events_connect] current_user.api_id=" + str(current_user.api_id))
        print("[events_connect] current_user.database_id=" + str(current_user.database_id))
        
        emit('socket_set_userid', {'userid': userid, "user_database_id":current_user.database_id}, to=request.sid)
    else:
        emit('socket_set_userid', {'userid': userid, "user_database_id":0}, to=request.sid)

@io.on('disconnect')
def test_disconnect():
    pass
    
#----------------------------------------------------------------------------------------------
def run_app():
    global app
    Mobility(app)
    
    CORS(app, resources={r"/*":{"origins":"*"}})

    app.secret_key = 'xxxxyyyyyzzzzz'
    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = "xxxxxtttttt"
    #app.config['SERVER_NAME'] = 'localhost:8080'
    app.config['BABEL_DEFALUT_LOCALE'] = 'en'
    base_dir = os.path.abspath(os.path.dirname(__file__))
    
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = base_dir + '/translations'
    print("translations dir : " + app.config['BABEL_TRANSLATION_DIRECTORIES'])

    app.config['LANGUAGES'] =  {
                'en': 'English',
                'uk_UA': 'Ukrainian',
            }
    #app.jinja_env = environment() #Environment(extensions=['jinja2.ext.i18n'])

    env = app.jinja_env
    env.add_extension('jinja2.ext.do')
    env.add_extension('jinja2.ext.i18n')

#----------------------------------------------------------------------------------------------
def import_libs():
    pass

#----------------------------------------------------------------------------------------------
def bin_loaded():
    pass

#----------------------------------------------------------------------------------------------
def runtime_test_enabled():
    return 'USE_TEST_RUNTIME' in os.environ
    #return True

#----------------------------------------------------------------------------------------------
def start_service():

    print("[start_service]:run")
    pass

#----------------------------------------------------------------------------------------------
def get_user_agent_folder():
    if request.user_agent.platform in ['android', 'iphone', 'ipad', 'windows phone']:
        return "mobile"
    return "desktop"

#----------------------------------------------------------------------------------------------
def get_locales():
    global _app_locale
    return {'id' : '0',
            'ver': '0', 
            'locale': ''}
