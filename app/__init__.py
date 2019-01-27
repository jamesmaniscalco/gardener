import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix


def create_app():
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config')    # global configuration
    app.config.from_pyfile('config.py', silent=True)    # instance-specific configuration

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'Hello, World!'

    # WSGI setup
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # database connections
    from . import db
    db.init_app(app)

    return app

    