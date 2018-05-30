from flask import Flask
from routes import db
from routes.user import user_routes
from routes.admin import admin_routes
from flask_jwt_extended import JWTManager
from app.config import config


def initialize_app(config_name="DEVELOPMENT"):
    app = Flask(__name__, instance_relative_config=True)
    """ Load the app configuration"""
    app.config.from_object(config[config_name])
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")
    app.register_blueprint(admin_routes, url_prefix="/api/v1/admin")

    # initialize JWT
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        return token['jti'] in db.blacklist

    return app
