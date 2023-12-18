"""The main application"""
from flask_jwt_extended import JWTManager
from v1.routes import db
from v1.routes.user import user_routes
from v1.routes.admin import admin_routes
from v1.routes.web import web


def initialize_app(app):
    # initialize JWT
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_token(token):
        """check if the token is blacklisted"""
        return token['jti'] in db.blacklist

    return app


def clear():
    """Clear the non-persistent data storage"""
    db.clear()
