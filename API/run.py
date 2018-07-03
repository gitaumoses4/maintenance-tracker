""" Initializes and runs the application"""
from dotenv import load_dotenv
from flask import Flask, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_mail import Mail

import v1
from config import config
from v1 import user_routes, admin_routes, web
from v2.app.database import Database, MailSender
from flask_cors import CORS

db = Database()
mail_sender = MailSender()
import v2.app.routes
from migrate import Migration

load_dotenv()


def create_app(config_name="DEVELOPMENT"):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app)
    app.config.from_object(config[config_name])

    v1.initialize_app(app)
    app.register_blueprint(user_routes, url_prefix="/api/v1/users")
    app.register_blueprint(admin_routes, url_prefix="/api/v1/admin")
    app.register_blueprint(web)
    app.register_blueprint(v2.app.routes.resource_routes, url_prefix="/api/v2")
    db.init_app(app)
    mail_sender.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        from v2.app.models import Blacklist
        """check if the token is blacklisted"""
        return Blacklist.query_one_by_field("token", token['jti']) is not None

    @jwt.expired_token_loader
    def my_expired_token_callback():
        return jsonify({
            'status': "error",
            'message': 'The token has expired, login to get another token'
        }), 401

    @jwt.unauthorized_loader
    def unauthorized(e):
        return jsonify({
            "status": "error",
            "message": "Bearer token not provided"
        }), 401

    @jwt.invalid_token_loader
    def invalid_token(e):
        return jsonify({
            "status": "error",
            "message": "Invalid token provided"
        }), 401

    @app.route("/")
    def get_home_page():
        return send_from_directory("./docs", "index.html")

    @app.route("/css")
    def get_css():
        return send_from_directory("./docs", "mg-framework.css")

    @app.route('/js')
    def get_js():
        return send_from_directory("./docs", "mg-framework.js")

    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    return app


app = create_app()
migration = Migration()
migration.set_up()
if __name__ == '__main__':
    app.run()
