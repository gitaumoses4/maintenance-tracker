""" Initializes and runs the application"""
from flask import Flask
import v1, v2
from config import config


def create_app(config_name="DEVELOPMENT"):
    """Initializes the application"""
    application = Flask(__name__, instance_relative_config=True)
    application.config.from_object(config[config_name])
    v1.initialize_app(application)

    return application


app = create_app()
if __name__ == '__main__':
    app.run()
