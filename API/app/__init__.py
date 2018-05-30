from flask import Flask
from app.config import config

app = Flask(__name__, instance_relative_config=True)


def initialize_app(config_name="DEVELOPMENT"):
    """ Load the app configuration"""
    app.config.from_object(config[config_name])

    return app
