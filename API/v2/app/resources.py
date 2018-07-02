"""
The main resources for the API endpoints
"""
import math
import os
import re
from datetime import datetime
from functools import wraps

from flask import request, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, get_jwt_identity
from flask_restful import Resource
from passlib.handlers.bcrypt import bcrypt
from werkzeug.utils import secure_filename

from v2.app.models import User, Blacklist, Request, Feedback, Notification

RESULTS_PER_PAGE = 8  # define the maximum results per page


def get_page():
    if request.args.get("page") is not None:
        return int(request.args.get("page"))
    return 1


def paginated_results(total_results, items, items_key="items"):
    return {"status": "success", "data": {
        "current_page": get_page(),
        "num_results": len(items),
        "last_page": math.ceil(total_results / RESULTS_PER_PAGE),
        "total_results": total_results,
        items_key: [x.to_json_object_filter_fields(get_fields()) for x in items]
    }}, 200


def get_fields():
    if request.args.get("fields") is not None:
        return request.args.get("fields").split(",")
    return None


def admin_guard(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        user = User.query_by_id(get_jwt_identity())
        if not user.is_admin():
            return {"status": "error", "message": "User not an Admin"}, 401
        return f(*args, **kwargs)

    return wrapped


class UserResource(Resource):

    @jwt_required
    def get(self):
        user = User.query_by_id(get_jwt_identity())
        return {"status": "success", "data": {"user": user.to_json_object_filter_fields(get_fields())}}, 200

    @jwt_required
    @admin_guard
    def put(self, user_id):
        user = User.query_by_id(user_id)
        if user is None:
            return {"status": "error", "message": "User not found"}, 404
        user.role = User.ROLE_ADMINISTRATOR
        user.update()

        notification = Notification(
            admin=get_jwt_identity(), user=user.id,
            message="You have been upgraded to be an Administrator")
        notification.save()

        return {"status": "success", "message": "User is now an admin"}, 200


class UsersResource(Resource):

    @jwt_required
    @admin_guard
    def get(self):
        users = User.query_all(get_page(), RESULTS_PER_PAGE)

        total_results = User.count_all()
        return paginated_results(total_results, users, "users")


class UserSignUp(Resource):
    """
    Resource to perform user sign up
    """

    def is_valid(self, item):
        """Check if the response has valid user details"""
        errors = []
        if not item.get("firstname"):
            errors.append("First name is required")

        if not item.get("lastname"):
            errors.append("Last name is required")

        if not item.get("username"):
            errors.append("Username is required")
        elif len(User.query_by_field(field="username", value=item.get("username"))) != 0:
            errors.append("Username is already in use")

        if not item.get("email"):
            errors.append("Email is required")
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', item.get("email")) is None:
            errors.append("Not a valid email")
        elif len(User.query_by_field(field="email", value=item.get("email"))) != 0:
            errors.append("Email already in use")

        if not item.get("password"):
            errors.append("Password is required")
        elif len(item.get("password")) < 8:
            errors.append("Password must be more than 8 characters long")

        return len(errors) == 0, errors

    def post(self):
        if request.is_json:
            valid, errors = self.is_valid(request.json)
            if not valid:
                return {"message": errors, "status": "error"}, 400
            # create user
            result = request.json
            user = User(
                result['firstname'], result['lastname'], result[
                    'email'], result['username'],
                bcrypt.encrypt(result['password']))
            user.save()

            return {"data": {"user": user.to_json_object_filter_fields(get_fields())}, "status": "success"}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserLogin(Resource):

    def post(self):
        if request.is_json:
            if not request.json.get('username'):
                return {"status": "error", "message": ["Username is required"]}, 400
            if not request.json.get("password"):
                return {"status": "error", "message": ["Password is required"]}, 400
            user = User.query_one_by_field(
                "username", request.json.get("username"))
            if user is None or not bcrypt.verify(request.json.get("password"), user.password):
                return {"status": "error", "message": ["Invalid credentials"]}, 400
            access_token = create_access_token(identity=user.id)
            return {"status": "success",
                    "data": {"token": access_token, "user": user.to_json_object_filter_fields(get_fields())}}, 200
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserLogout(Resource):

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        blacklist = Blacklist(jti)
        blacklist.save()
        return {"status": "success", "message": "Successfully logged out"}, 200


class UserMaintenanceRequest(Resource):

    @staticmethod
    def is_valid(item):
        """Check if a request has valid fields"""
        errors = []
        if not item.get("product_name"):
            errors.append("Product name must be provided")

        if not item.get("description"):
            errors.append("Maintenance/Repair request description must be provided")

        return len(errors) == 0, errors

    @jwt_required
    def post(self):
        if request.is_json:
            valid, errors = self.is_valid(request.json)
            if not valid:
                return {"status": "error", "message": errors}, 400
            result = request.json
            maintenance_request = Request(product_name=result['product_name'],
                                          description=result['description'],
                                          created_by=get_jwt_identity())
            if result.get('photo'):
                maintenance_request.photo = result['photo']

            maintenance_request.save()

            return {"status": "success",
                    "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400

    @jwt_required
    def get(self, status):
        requests, num_results = Request.query_and_filter(request.args.get("from"), request.args.get("to"),
                                                         request.args.get("query"), status,
                                                         number_of_items=RESULTS_PER_PAGE, page=get_page(),
                                                         user_id=get_jwt_identity())

        return paginated_results(total_results=num_results, items=requests, items_key="requests")


class UserModifyRequest(Resource):

    def is_valid(self, maintenance_request, item):
        errors = []
        if not item.get("product_name"):
            errors.append("Product name must be provided")

        if not item.get("description"):
            errors.append("Maintenance/Repair request description must be provided")

        if maintenance_request.product_name == item.get("product_name") and \
                maintenance_request.description == item.get("description"):
            errors.append("The details entered already exist.")

        return len(errors) == 0, errors

    @jwt_required
    def get(self, request_id):
        maintenance_request = Request.query_by_id(request_id)
        if maintenance_request is None:
            return {"status": "error", "message": "Maintenance request does not exist"}, 404
        elif maintenance_request.created_by == get_jwt_identity() or User.query_by_id(
                get_jwt_identity()).is_admin():
            maintenance_request.created_by = User.query_by_id(get_jwt_identity()).to_json_object_filter_fields(
                ["id", "firstname", "lastname"])
            return {"status": "success",
                    "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 200
        else:
            return {"status": "error",
                    "message": "You are not allowed to modify or view this maintenance request "}, 401

    @jwt_required
    def put(self, request_id):
        if request.is_json:
            maintenance_request = Request.query_by_id(request_id)
            if maintenance_request is None:
                return {"status": "error", "message": "Maintenance request does not exist"}, 404
            elif maintenance_request.created_by != get_jwt_identity():
                return {"status": "error",
                        "message": "You are not allowed to modify or view this maintenance request"}, 401
            elif maintenance_request.status != Request.STATUS_PENDING:
                return {"status": "error",
                        "message": "A maintenance request can only be edited if pending."}, 400
            valid, errors = self.is_valid(maintenance_request, request.json)
            if not valid:
                return {"status": "error", "message": errors}, 400
            result = request.json

            maintenance_request.product_name = result['product_name']
            maintenance_request.description = result['description']

            maintenance_request.update()
            return {"status": "success",
                    "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 200
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class AdminMaintenanceRequest(Resource):

    @jwt_required
    @admin_guard
    def get(self, status):
        requests, total_results = Request.query_and_filter(request.args.get("from"), request.args.get("to"),
                                                           request.args.get("query"), status,
                                                           number_of_items=RESULTS_PER_PAGE, page=get_page())

        return paginated_results(total_results=total_results,
                                 items=requests,
                                 items_key="requests")


class AdminManageRequest(Resource):

    @jwt_required
    @admin_guard
    def put(self, request_id, status):
        statuses = {
            "approve": Request.STATUS_APPROVED, "disapprove": Request.STATUS_DISAPPROVED,
            "pending": Request.STATUS_PENDING, "resolve": Request.STATUS_RESOLVED}
        if status not in statuses.keys():
            return {"status": "error",
                    "message": "Request status can only be [approve,resolve,disapprove]"}, 400

        maintenance_request = Request.query_by_id(request_id)
        if maintenance_request is None:
            return {"status": "error", "message": "Maintenance request does not exist"}, 404
        elif status == 'approve' and maintenance_request.status != Request.STATUS_PENDING:
            return {"status": "error",
                    "message": "Only a pending request can be approved"}, 400

        maintenance_request.status = statuses[status]

        maintenance_request.update()

        notification = Notification(
            admin=get_jwt_identity(), user=maintenance_request.created_by,
            message="Maintenance Request with ID #{0} has been {1}".format(request_id, statuses[status]))
        notification.save()
        return {"status": "success",
                "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 200


class AdminFeedback(Resource):

    @staticmethod
    def is_valid(item):
        """Check whether a feedback object has valid fields"""
        errors = []
        if not item.get("message"):
            errors.append("Feedback message must be provided")

        return len(errors) == 0, errors

    @jwt_required
    @admin_guard
    def post(self, request_id):
        if request.is_json:
            maintenance_request = Request.query_by_id(request_id)
            if maintenance_request is None:
                return {"status": "error", "message": "Maintenance request does not exist"}, 404
            else:
                valid, errors = self.is_valid(request.json)
                if not valid:
                    return {"status": "error", "message": errors}, 400
                else:
                    feedback = Feedback(
                        admin=get_jwt_identity(), request=maintenance_request.id,
                        message=request.json.get("message"))
                    feedback.save()
                    notification = Notification(
                        admin=get_jwt_identity(), user=maintenance_request.created_by,
                        message="Feedback provided for Request #{0}".format(request_id))
                    notification.save()
                    return {"status": "success",
                            "data": {"feedback": feedback.to_json_object_filter_fields(get_fields())}}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserAllFeedbackResource(Resource):
    @jwt_required
    def get(self):
        feedback, num_results = Feedback.all_for_user(get_jwt_identity(), number_of_items=RESULTS_PER_PAGE,
                                                      page=get_page())
        for f in feedback:
            f.admin = f.created_by().to_json_object_filter_fields(['id', 'firstname', 'lastname'])

        return paginated_results(num_results, items=feedback, items_key="feedback")


class UserFeedbackResource(Resource):

    @jwt_required
    def get(self, request_id):
        maintenance_request = Request.query_by_id(request_id)
        if maintenance_request is None:
            return {"status": "error", "message": "Maintenance request does not exist"}, 404
        elif maintenance_request.created_by != get_jwt_identity() or not User.query_by_id(
                get_jwt_identity()).is_admin():
            feedback = [{"feedback": x.to_json_object_filter_fields(get_fields()),
                         "created_by": x.created_by().to_json_object_filter_fields(["id", "firstname", "lastname"])} for
                        x
                        in maintenance_request.feedback()]
            return {"status": "success",
                    "data": feedback}, 200
        else:
            return {"status": "error",
                    "message": "You are not allowed to modify or view this maintenance request"}, 401


class NotificationResource(Resource):

    @jwt_required
    def get(self, status):
        user = User.query_by_id(get_jwt_identity())
        if status == "read":
            notifications = user.read_notifications()
        elif status == "unread":
            notifications = user.unread_notifications()
        else:
            notifications = user.notifications()

        for notification in notifications:
            notification.admin = notification.get_admin().to_json_object_filter_fields(
                ['firstname', 'lastname', 'id'])

        return paginated_results(len(notifications), items=notifications, items_key="notifications")


class ManageNotifications(Resource):

    @jwt_required
    def get(self, notification_id):
        notification = Notification.query_by_id(notification_id)
        if not notification:
            return {"status": "error", "message": "Notification not found"}, 404
        if notification.user != get_jwt_identity():
            return {"status": "error",
                    "message": "You are not allowed to modify or view this notification"}, 401
        else:
            return {"status": "success",
                    "data": {"notification": notification.to_json_object_filter_fields(get_fields())}}, 200

    @jwt_required
    def put(self, notification_id):
        notification = Notification.query_by_id(notification_id)
        if not notification:
            return {"status": "error", "message": "Notification not found"}, 404
        if notification.user != get_jwt_identity():
            return {"status": "error",
                    "message": "You are not allowed to modify or view this notification"}, 401
        else:
            notification.mark_as_read()
            return {"status": "success",
                    "data": {"notification": notification.to_json_object_filter_fields(get_fields())}}, 200

    @jwt_required
    @admin_guard
    def post(self, user_id):
        if request.is_json:
            user = User.query_by_id(user_id)
            if user is None:
                return {"status": "error", "message": "User does not exist"}, 404
            else:
                if request.json.get("message") is None:
                    return {"status": "error", "data": {"message": "Notification message is required"}}, 400
                else:
                    notification = Notification(
                        admin=get_jwt_identity(), user=user.id,
                        message=request.json.get("message"))
                    notification.save()
                    return {"status": "success",
                            "data": {
                                "notification": notification.to_json_object_filter_fields(get_fields())}}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400
