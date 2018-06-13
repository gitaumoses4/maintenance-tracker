"""
The main resources for the API endpoints
"""
import re
from functools import wraps

from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt, get_jwt_identity
from flask_restful import Resource
from passlib.handlers.bcrypt import bcrypt

from v2.app.models import User, Blacklist, Request, Feedback, Notification

RESULTS_PER_PAGE = 10  # define the maximum results per page


def get_page():
    if request.args.get("page") is not None:
        return int(request.args.get("page"))
    return 1


def paginated_results(total_results, items, items_key="items"):
    previous_page = None
    next_page = None
    if get_page() > 1:
        previous_page = "{0}?page={1}".format(request.url_rule, (get_page() - 1))

    if get_page() < (total_results / RESULTS_PER_PAGE):
        next_page = "{0}?page={1}".format(request.url_rule, (get_page() + 1))
    return {"status": "success", "data": {
        "current_page": get_page(),
        "previous_page": previous_page,
        "next_page": next_page,
        "num_results": len(items),
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
        errors = {}
        if not item.get("firstname"):
            errors['firstname'] = "First name is required"

        if not item.get("lastname"):
            errors['lastname'] = "Last name is required"

        if not item.get("username"):
            errors['username'] = "Username is required"
        elif len(User.query_by_field(field="username", value=item.get("username"))) != 0:
            errors['username'] = "Username is already in use"

        if not item.get("email"):
            errors['email'] = "Email is required"
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', item.get("email")) is None:
            errors["email"] = "Not a valid email"
        elif len(User.query_by_field(field="email", value=item.get("email"))) != 0:
            errors["email"] = "Email already in use"

        if not item.get("password"):
            errors["password"] = "Password is required"
        elif len(item.get("password")) < 8:
            errors["password"] = "Password must be more than 8 characters long"

        return len(errors) == 0, errors

    def post(self):
        if request.is_json:
            valid, errors = self.is_valid(request.json)
            if not valid:
                return {"data": errors, "status": "error"}, 400
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
                return {"status": "error", "data": {"username": "Username is required"}}, 400
            if not request.json.get("password"):
                return {"status": "error", "data": {"email": "Password is required"}}, 400
            user = User.query_one_by_field(
                "username", request.json.get("username"))
            if user is None:
                return {"status": "error", "message": "Username does not exist"}, 400
            elif not bcrypt.verify(request.json.get("password"), user.password):
                return {"status": "error", "message": "Wrong password"}, 400
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
        errors = {}
        if not item.get("product_name"):
            errors["product_name"] = "Product name must be provided"

        if not item.get("description"):
            errors[
                "description"] = "Maintenance/Repair request description must be provided"

        return len(errors) == 0, errors

    @jwt_required
    def post(self):
        if request.is_json:
            valid, errors = self.is_valid(request.json)
            if not valid:
                return {"status": "error", "data": errors}, 400
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
        if status == "pending" or status == "approved" or status == "disapproved" or status == "resolved":
            requests = [x for x in
                        Request.query_by_field("created_by", get_jwt_identity(), get_page(), RESULTS_PER_PAGE) if
                        x.status.lower() == status]
            num_results = len([x for x in Request.query_for_user(get_jwt_identity()) if x.status.lower() == status])
        elif status == "all":
            num_results = Request.count_all_by_field("created_by", get_jwt_identity())
            requests = Request.query_by_field("created_by", get_jwt_identity(), get_page(), RESULTS_PER_PAGE)
        else:
            num_results = 0
            requests = []
        return paginated_results(total_results=num_results, items=requests, items_key="requests")


class UserModifyRequest(Resource):

    def is_valid(self, maintenance_request, item):
        errors = {}
        if not item.get("product_name"):
            errors["product_name"] = "Product name must be provided"

        if not item.get("description"):
            errors[
                "description"] = "Maintenance/Repair request description must be provided"

        if maintenance_request.product_name == item.get("product_name") and \
                maintenance_request.description == item.get("description"):
            errors['fields'] = "The details entered already exist."

        return len(errors) == 0, errors

    @jwt_required
    def get(self, request_id):
        maintenance_request = Request.query_by_id(request_id)
        if maintenance_request is None:
            return {"status": "error", "message": "Maintenance request does not exist"}, 404
        elif maintenance_request.created_by != get_jwt_identity():
            return {"status": "error", "message": "You are not allowed to modify or view this maintenance request"}, 401
        else:
            return {"status": "success",
                    "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 200

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
                return {"status": "error", "data": errors}, 400
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
        if status in ["pending", "approved", "disapproved", "resolved"]:
            requests = [x for x in Request.query_all(page=get_page(), number_of_items=RESULTS_PER_PAGE)
                        if x.status.lower() == status]
            total_results = len([x for x in Request.query_all() if x.status.lower() == status])
        elif status == "all":
            requests = Request.query_all(page=get_page(), number_of_items=RESULTS_PER_PAGE)
            total_results = Request.count_all()
        else:
            requests = []
            total_results = 0

        return paginated_results(total_results=total_results,
                                 items=requests, items_key="requests")


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
        return {"status": "success",
                "data": {"request": maintenance_request.to_json_object_filter_fields(get_fields())}}, 200


class AdminFeedback(Resource):

    @staticmethod
    def is_valid(item):
        """Check whether a feedback object has valid fields"""
        errors = {}
        if not item.get("message"):
            errors["message"] = "Feedback message must be provided"

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
                    return {"status": "error", "data": errors}, 400
                else:
                    feedback = Feedback(
                        admin=get_jwt_identity(), request=maintenance_request.id,
                        message=request.json.get("message"))
                    feedback.save()
                    return {"status": "success",
                            "data": {"feedback": feedback.to_json_object_filter_fields(get_fields())}}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserFeedbackResource(Resource):

    @jwt_required
    def get(self, request_id):
        maintenance_request = Request.query_by_id(request_id)
        if maintenance_request is None:
            return {"status": "error", "message": "Maintenance request does not exist"}, 404
        elif maintenance_request.created_by != get_jwt_identity():
            return {"status": "error",
                    "message": "You are not allowed to modify or view this maintenance request"}, 401
        else:
            feedback = maintenance_request.feedback()
            return {"status": "success",
                    "data": {"feedback": [x.to_json_object_filter_fields(get_fields()) for x in feedback]}}, 200


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
