"""The main application"""
from flask import Flask
from flask_jwt_extended import JWTManager
from routes import db
from routes.user import user_routes
from routes.admin import admin_routes
from app.config import config


def initialize_app(config_name="DEVELOPMENT"):
    """ Load the app configuration"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")
    app.register_blueprint(admin_routes, url_prefix="/api/v1/admin")

    # initialize JWT
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        """check if the token is blacklisted"""
        return token['jti'] in db.blacklist

    check_token("")
    return app


def clear():
    """Clear the non-persistent data storage"""
    db.clear()
