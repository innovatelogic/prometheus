import os
from jinja2 import Environment
from flask import Flask
from flask import session, request
from flask_login import LoginManager
from flask_babel import Babel, gettext
from app import app, babel_, import_libs, start_service, run_app
from app.config.settings import LANGUAGES


jinja_env = Environment(extensions=['jinja2.ext.i18n'])

os.environ.setdefault('FLASK_ENV', 'development')
os.environ.pop("FLASK_RUN_FROM_CLI", None)
os.environ.pop("FLASK_ENV", None)


#----------------------------------------------------------------------------------------------
#@babel_.localeselector
def get_locale_():
    print("get_locale")
    return "UK"

#----------------------------------------------------------------------------------------------
def create_app():
    global app

    import_libs()
    start_service()
    run_app()

    from app.py import routes

    return app


