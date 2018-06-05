"""The main application file"""

from flask import Flask
from app.config import config


def initialize_app(config_name="DEVELOPMENT"):
    """ Create the app and register blueprints"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    return app
