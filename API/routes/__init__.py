from models import User, Admin
from flask import jsonify, request, Blueprint
from data_store import MaintenanceTrackerDB
import json
from passlib.hash import bcrypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt)

routes = Blueprint("routes", __name__)
db = MaintenanceTrackerDB()


@routes.route("/users/signup", methods=["POST"])
def register_user():
    if not request.is_json:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
    valid, errors = db.users.is_valid(request.json)
    if not valid:
        return jsonify({
            "data": errors,
            "status": "error"
        }), 400
    # create user
    result = request.json
    user = User(result['firstname'], result['lastname'], result['email'], result['username'], result['password'])

    db.users.insert(user)
    return jsonify({
        "data": {
            "user": user.to_json_object()
        },
        "status": "success"
    }), 201
