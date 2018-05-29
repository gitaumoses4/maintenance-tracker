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


def is_json():
    if not request.is_json:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
    return True


@routes.route("/users/signup", methods=["POST"])
def register_user():
    if is_json():
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


@routes.route("/users/login", methods=["POST"])
def login_user():
    if is_json():
        if not request.json.get('username'):
            return jsonify({
                "status": "error",
                "data": {
                    "username": "Username is required"
                }
            }), 400
        if not request.json.get("password"):
            return jsonify({
                "status": "error",
                "data": {
                    "email": "Password is required"
                }
            }), 400

        user = db.users.query_by_field("username", request.json.get("username"))
        if not user:
            return jsonify({
                "status": "error",
                "message": "Username does not exist"
            }), 400
        elif not bcrypt.verify(request.json.get("password"), user.password):
            return jsonify({
                "status": "error",
                "message": "Wrong password"
            }), 400

        access_token = create_access_token(identity=user.username)
        return jsonify({
            "status": "success",
            "data": {
                "token": access_token
            }
        }), 200
