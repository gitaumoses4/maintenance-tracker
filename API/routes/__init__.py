from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from data_store.db import MaintenanceTrackerDB

db = MaintenanceTrackerDB()


def is_json():
    if not request.is_json:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
    return True


@jwt_required
def get_current_user():
    return db.users.query_by_field("username", get_jwt_identity())


def validate(validator):
    errors = {}
    for key in validator:
        if not request.json.get(key):
            errors[key] = validator[key]
    if len(errors) > 0:
        return False, jsonify({
            "status": "error",
            "data": errors
        }), 400
    else:
        return True, None, None
