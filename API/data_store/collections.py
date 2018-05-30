import re
from datetime import datetime

from passlib.handlers.bcrypt import bcrypt

from models.base import BaseModel
from models.user import User


class NonPersistentCollection:
    data = {}
    index = 1

    def query_all(self):
        return self.data

    def query_all_where_field_eq(self, field, value):
        result = []
        for item in self.data.values():
            if item.to_json_object()[field] == value:
                result.append(item)

        return result

    def insert(self, item):
        assert isinstance(item, BaseModel)
        item.created_at = datetime.now()
        self.data[self.index] = item
        item.id = self.index
        self.index += 1

    def set(self, item, item_id):
        assert isinstance(item, BaseModel)
        item.updated_at = datetime.now()
        self.data[item_id] = item

    def query(self, item_id):
        return self.data.get(item_id)

    def query_by_field(self, field, value):
        for item in self.data.values():
            if item.to_json_object()[field] == value:
                return item

    def delete(self, item_id):
        del self.data[item_id]

    def is_valid(self, item):
        return True, []

    def clear(self):
        self.data = {}


class UserCollection(NonPersistentCollection):

    def insert(self, item):
        # encrypt the password
        assert isinstance(item, User)
        item.password = bcrypt.encrypt(item.password)

        # now insert item
        super().insert(item)

    def is_valid(self, item):
        errors = {}
        if not item.get("firstname"):
            errors['firstname'] = "First name is required"

        if not item.get("lastname"):
            errors['lastname'] = "Last name is required"

        if not item.get("username"):
            errors['username'] = "Username is required"
        elif self.query_by_field(field="username", value=item.get("username")) is not None:
            errors['username'] = "Username is already in use"

        if not item.get("email"):
            errors['email'] = "Email is required"
        elif re.match(r'^.+@([?)[a-zA-Z0-9-.])+.([a-zA-Z]{2,3}|[0-9]{1,3})(]?)$', item.get("email")) is None:
            errors["email"] = "Not a valid email"
        elif self.query_by_field(field="email", value=item.get("email")) is not None:
            errors["email"] = "Email already in use"

        if not item.get("password"):
            errors["password"] = "Password is required"
        elif len(item.get("password")) < 8:
            errors["password"] = "Password must be more than 8 characters long"

        return len(errors) == 0, errors


class RequestCollection(NonPersistentCollection):
    def is_valid(self, item):
        errors = {}
        if not item.get("product_name"):
            errors["product_name"] = "Product name must be provided"

        if not item.get("description"):
            errors["description"] = "Maintenance/Repair request description must be provided"

        return len(errors) == 0, errors


class NotificationCollection(NonPersistentCollection):
    def is_valid(self, item):
        errors = {}
        if not item.get("message"):
            errors["message"] = "Notification message must be provided"

        return len(errors) == 0, errors


class FeedbackCollection(NonPersistentCollection):
    def is_valid(self, item):
        errors = {}
        if not item.get("message"):
            errors["message"] = "Feedback message must be provided"

        return len(errors) == 0, errors
