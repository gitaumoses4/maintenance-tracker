""" Initializes and runs the application"""
from dotenv import load_dotenv
from flask import Flask

import v1
from config import config
from v1 import user_routes, admin_routes, web
from v2.database import Database

db = Database()

import v2.routes

load_dotenv()


def create_app(config_name="DEVELOPMENT"):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])

    v1.initialize_app(app)
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")
    app.register_blueprint(admin_routes, url_prefix="/api/v1/admin")
    app.register_blueprint(web)
    app.register_blueprint(v2.routes.resource_routes, url_prefix="/api/v2")
    db.init_app(app)

    return app


app = create_app()


if __name__ == '__main__':
    app.run()
