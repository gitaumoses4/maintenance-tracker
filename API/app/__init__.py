from flask import Flask
from config import config
from routes import routes

app = Flask(__name__, instance_relative_config=True)


def initialize_app(config_name="DEVELOPMENT"):
    """ Load the app configuration"""
    app.config.from_object(config[config_name])
    app.register_blueprint(routes, url_prefix="/api/v1")

    return app
