""" Initializes and runs the application"""
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

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

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        from v2.models import Blacklist
        """check if the token is blacklisted"""
        return Blacklist.query_one_by_field("token", token['jti']) is not None

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
