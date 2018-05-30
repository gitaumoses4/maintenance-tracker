from models.user import User
from models.request import Request
from flask import jsonify, request, Blueprint
from data_store.db import MaintenanceTrackerDB
import json
from routes import is_json, db, validate, get_current_user
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


@user_routes.route("/requests", methods=["POST"])
@jwt_required
def create_request():
    if is_json():
        valid, errors = db.requests.is_valid(request.json)
        if not valid:
            return jsonify({
                "status": "error",
                "data": errors
            })
        result = request.json
        maintenance_request = Request(product_name=result['product_name'],
                                      description=result['description'],
                                      created_by=get_current_user())
        if result.get('photo'):
            maintenance_request.photo = result['photo']

        db.requests.insert(maintenance_request)

        return jsonify({
            "status": "success",
            "data": {
                "request": maintenance_request.to_json_object()
            }
        }), 201


@user_routes.route("/requests", methods=["GET"])
@jwt_required
def get_all_requests():
    if is_json():
        requests = [x.to_json_object() for x in db.requests.query_all().values() if
                    x.created_by.username == get_jwt_identity()]  # get requests for this user
        return jsonify({
            "status": "success",
            "data": {
                "total_requests": len(requests),
                "requests": requests
            }
        }), 200


@user_routes.route("/requests/<int:_id>", methods=["PUT", "GET"])
@jwt_required
def modify_request(_id):
    if is_json():
        maintenance_request = db.requests.query(_id)
        if maintenance_request is None:
            return jsonify({
                "status": "error",
                "message": "Maintenance request does not exist"
            }), 404
        elif maintenance_request.created_by.username != get_jwt_identity():
            return jsonify({
                "status": "error",
                "message": "You are not allowed to modify or view this maintenance request"
            }), 401
        else:
            if request.method == "PUT":
                valid, errors = db.requests.is_valid(request.json)
                if not valid:
                    return jsonify({
                        "status": "error",
                        "data": errors
                    })
                result = request.json

                maintenance_request.product_name = result['product_name']
                maintenance_request.description = result['description']

            return jsonify({
                "status": "success",
                "data": maintenance_request.to_json_object()
            }), 200


@user_routes.route("/requests/<int:_id>/feedback", methods=['GET'])
@jwt_required
def get_feedback_for_request(_id):
    maintenance_request = db.requests.query(_id)
    print(get_jwt_identity())
    if maintenance_request is None:
        return jsonify({
            "status": "error",
            "message": "Maintenance request does not exist"
        }), 404
    elif maintenance_request.created_by.username != get_jwt_identity():
        return jsonify({
            "status": "error",
            "message": "You are not allowed to modify or view this maintenance request"
        }), 401
    else:
        feedback = [x.to_json_object() for x in db.feedback.query_all().values() if x.request.id == _id]
        return jsonify({
            "status": "success",
            "data": {
                "feedback": feedback
            }
        }), 200
