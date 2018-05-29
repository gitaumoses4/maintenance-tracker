from flask import Flask
from config import config
from routes import routes, db
from flask_jwt_extended import JWTManager

app = Flask(__name__, instance_relative_config=True)


def initialize_app(config_name="DEVELOPMENT"):
    """ Load the app configuration"""
    app.config.from_object(config[config_name])
    app.register_blueprint(routes, url_prefix="/api/v1")

    # initialize JWT
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_token(token):
        return token['jti'] in db.blacklist

    return app
