from flask import jsonify, request
from data_store.db import MaintenanceTrackerDB

db = MaintenanceTrackerDB()


def is_json():
    if not request.is_json:
        return jsonify({
            "message": "Request should be in JSON",
            "status": "error"
        }), 400
    return True
