import json
from datetime import datetime
import os


class BaseModel:

    def __init__(self, created_at, updated_at):
        self.created_at = created_at
        self.updated_at = updated_at

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class User(BaseModel):
    ROLE_ADMINISTRATOR = "Administrator"
    ROLE_USER = "User"

    def __init__(self, firstname="", lastname="", email="", username="", password="", profile_picture="",
                 created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.username = username
        self.password = password
        self.profile_picture = profile_picture
        self.role = User.ROLE_USER


class Admin(User):
    def __init__(self, firstname="", lastname="", email="", username="", password="", profile_picture="",
                 created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(firstname, lastname, email, username, password, profile_picture, created_at, updated_at)
        self.role = User.ROLE_ADMINISTRATOR

    @staticmethod
    def default():
        admin = Admin()
        admin.firstname = os.getenv("DEFAULT_ADMIN_FIRST_NAME")
        admin.lastname = os.getenv("DEFAULT_ADMIN_LAST_NAME")
        admin.email = os.getenv("DEFAULT_ADMIN_EMAIL")
        admin.password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        admin.profile_picture = os.getenv("DEFAULT_ADMIN_PROFILE_PICTURE")

        return admin


class Request(BaseModel):
    STATUS_PENDING = "Pending"
    STATUS_APPROVED = "Approved"
    STATUS_REJECTED = "Rejected"
    STATUS_RESOLVED = "Resolved"

    def __init__(self, product_name="", description="", status=STATUS_PENDING, photo="", created_by=None,
                 created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.product_name = product_name
        self.description = description
        self.status = status
        self.photo = photo
        self.created_by = created_by


class Feedback(BaseModel):
    def __init__(self, admin=None, request=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.request = request
        self.message = message


class Notification(BaseModel):
    def __init__(self, admin=None, user=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.user = user
        self.message = message
