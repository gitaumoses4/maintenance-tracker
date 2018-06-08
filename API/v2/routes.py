"""
The main endpoints for the application
"""
from flask_restful import Api
from flask import Blueprint

from v2.resources import UserSignUp, UserLogin, UserLogout

resource_routes = Blueprint("resource_routes", __name__)

api = Api(resource_routes)

api.add_resource(UserSignUp, "/auth/signup")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(UserLogout, "/auth/logout")
