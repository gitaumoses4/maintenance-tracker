from models.user import User
from models.admin import Admin
from flask import jsonify, request, Blueprint
from data_store.db import MaintenanceTrackerDB
import json
from routes import is_json, db
from passlib.hash import bcrypt
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    get_jwt_identity,
    get_raw_jwt)

user_routes = Blueprint("routes.user", __name__)


@user_routes.route("/signup", methods=["POST"])
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


@user_routes.route("/login", methods=["POST"])
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


@user_routes.route("/logout", methods=["DELETE"])
@jwt_required
def logout_user():
    jti = get_raw_jwt()['jti']
    db.blacklist.add(jti)
    return jsonify({
        "status": "success",
        "message": "Successfully logged out"
    }), 200
