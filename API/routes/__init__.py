from flask_jwt_extended import get_jwt_identity, jwt_required

from data_store.db import MaintenanceTrackerDB

db = MaintenanceTrackerDB()


@jwt_required
def get_current_user():
    return db.users.query_by_field("username", get_jwt_identity())
