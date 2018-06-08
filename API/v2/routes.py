"""
The main endpoints for the application
"""
from flask_restful import Api
from flask import Blueprint

from v2.resources import UserSignUp, UserLogin, UserLogout, UserMaintenanceRequest, UserModifyRequest, \
    AdminMaintenanceRequest, AdminManageRequest

resource_routes = Blueprint("resource_routes", __name__)

api = Api(resource_routes)

api.add_resource(UserSignUp, "/auth/signup")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(UserLogout, "/auth/logout")
api.add_resource(UserMaintenanceRequest, "/users/requests")
api.add_resource(UserModifyRequest, "/users/requests/<int:request_id>")
api.add_resource(AdminMaintenanceRequest, "/requests")
api.add_resource(AdminManageRequest, "/requests/<int:request_id>/<string:status>")
