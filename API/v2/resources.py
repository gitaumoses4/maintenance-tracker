"""
The main resources for the API endpoints
"""
import re
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from flask_restful import Resource
from passlib.handlers.bcrypt import bcrypt

from v2.models import User, Blacklist


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
            user = User(result['firstname'], result['lastname'], result['email'], result['username'],
                        bcrypt.encrypt(result['password']))
            user.save()

            return {"message": "Registration successful", "status": "success"}, 201
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserLogin(Resource):

    def post(self):
        if request.is_json:
            if not request.json.get('username'):
                return {"status": "error", "data": {"username": "Username is required"}}, 400
            if not request.json.get("password"):
                return {"status": "error", "data": {"email": "Password is required"}}, 400
            user = User.query_one_by_field("username", request.json.get("username"))
            if user is None:
                return {"status": "error", "message": "Username does not exist"}, 400
            elif not bcrypt.verify(request.json.get("password"), user.password):
                return {"status": "error", "message": "Wrong password"}, 400
            access_token = create_access_token(identity=user.username)
            return {"status": "success", "data": {"token": access_token, "user": user.to_json_object()}}, 200
        else:
            return {"message": "Request should be in JSON", "status": "error"}, 400


class UserLogout(Resource):

    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        blacklist = Blacklist(jti)
        blacklist.save()
        return {"status": "success", "message": "Successfully logged out"}, 200
