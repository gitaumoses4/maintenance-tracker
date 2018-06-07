"""
The main resources for the API endpoints
"""
import re
from flask import request
from flask_restful import Resource
from passlib.handlers.bcrypt import bcrypt

from v2.models import User


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
