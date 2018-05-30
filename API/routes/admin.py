from models.feedback import Feedback
from models.user import User
from routes import is_json, db, validate, get_current_user
from flask import jsonify, request, Blueprint
from passlib.hash import bcrypt
from flask_jwt_extended import (
    jwt_required,
    create_access_token,
    get_raw_jwt)

admin_routes = Blueprint("routes.admin", __name__)


@admin_routes.route("/login", methods=['POST'])
def login_admin():
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
        elif not user.role == User.ROLE_ADMINISTRATOR:
            return jsonify({
                "status": "error",
                "message": "User is not an admin"
            }), 401
        access_token = create_access_token(identity=user.username)
        return jsonify({
            "status": "success",
            "data": {
                "token": access_token
            }
        }), 200


@admin_routes.route("/logout", methods=["DELETE"])
@jwt_required
def logout_admin():
    jti = get_raw_jwt()['jti']
    db.blacklist.add(jti)
    return jsonify({
        "status": "success",
        "message": "Successfully logged out"
    }), 200


@admin_routes.route("/requests", methods=["GET"])
@jwt_required
def get_all_requests():
    if is_json():
        requests = [x.to_json_object() for x in db.requests.query_all().values()]
        return jsonify({
            "status": "success",
            "data": {
                "total_requests": len(requests),
                "requests": requests
            }
        }), 200


@admin_routes.route("/requests/<int:_id>", methods=["PUT", "GET"])
@jwt_required
def modify_request(_id):
    if is_json():
        maintenance_request = db.requests.query(_id)
        if maintenance_request is None:
            return jsonify({
                "status": "error",
                "message": "Maintenance request does not exist"
            }), 404
        else:
            if request.method == "PUT":
                valid, response, response_code = validate({"status": "Maintenance status is required"})
                if valid:
                    result = request.json
                    maintenance_request.status = result['status']
                else:
                    return response, response_code

            return jsonify({
                "status": "success",
                "data": maintenance_request.to_json_object()
            }), 200


@admin_routes.route('/requests/<int:_id>/feedback', methods=['POST'])
@jwt_required
def write_feedback_for_request(_id):
    if is_json():
        maintenance_request = db.requests.query(_id)
        if maintenance_request is None:
            return jsonify({
                "status": "error",
                "message": "Maintenance request does not exist"
            }), 404
        else:
            valid, errors = db.feedback.is_valid(request.json)
            if not valid:
                return jsonify({
                    "status": "error",
                    "data": errors
                }), 400
            else:
                feedback = Feedback(admin=get_current_user(), request=maintenance_request,
                                    message=request.json.get("message"))
                db.feedback.insert(feedback)
                return jsonify({
                    "status": "success",
                    "data": feedback.to_json_object()
                }), 201
