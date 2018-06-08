"""
The main endpoints for the application
"""
from flask_restful import Api
from flask import Blueprint

from v2.resources import UserSignUp

resource_routes = Blueprint("resource_routes", __name__)

api = Api(resource_routes)

api.add_resource(UserSignUp, "/auth/signup")
