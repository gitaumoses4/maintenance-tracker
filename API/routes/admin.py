from models.user import User
from models.admin import Admin
from routes import is_json, db
from flask import jsonify, request, Blueprint
import json
from passlib.hash import bcrypt
from flask_jwt_extended import (
    JWTManager,
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
