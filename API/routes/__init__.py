from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from data_store.db import MaintenanceTrackerDB

db = MaintenanceTrackerDB()


def is_json():
    if not request.is_json:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
    return True


def get_current_user():
    return db.users.query_by_field("username", get_jwt_identity())
