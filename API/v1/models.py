"""Models will be used to store the data in a data structure"""
import json
from datetime import datetime
from config import default_config


class BaseModel:
    """The base model class, creates common functionality between the models"""

    def __init__(self, created_at, updated_at):
        self.created_at = created_at
        self.updated_at = updated_at
        self.id = 0

    def to_json_object(self, exclude=True):
        return json.loads(self.to_json_str(exclude))

    def to_json_str(self, exclude=True):
        fields = self.excluded_fields()
        if not exclude:
            fields = []
        return json.dumps(self,
                          default=lambda o: o.strftime("%Y-%m-%d %H:%M:%S") if isinstance(o, datetime)
                          else {k: v for k, v in o.__dict__.items() if
                                k not in fields},
                          sort_keys=True, indent=4)

    def excluded_fields(self):
        return ['created_at', 'updated_at']


class User(BaseModel):
    """The user class"""
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

    def excluded_fields(self):
        return ['password', 'role', 'created_at', 'updated_at']


class Admin(User):
    """The Admin class"""

    def __init__(self, firstname="", lastname="", email="", username="", password="", profile_picture="",
                 created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(firstname, lastname, email, username, password, profile_picture, created_at, updated_at)
        self.role = User.ROLE_ADMINISTRATOR

    @staticmethod
    def default():
        admin = Admin()
        admin.firstname = default_config.DEFAULT_ADMIN_FIRST_NAME
        admin.lastname = default_config.DEFAULT_ADMIN_LAST_NAME
        admin.email = default_config.DEFAULT_ADMIN_EMAIL
        admin.username = default_config.DEFAULT_ADMIN_USER_NAME
        admin.password = default_config.DEFAULT_ADMIN_PASSWORD
        admin.profile_picture = default_config.DEFAULT_ADMIN_PROFILE_PICTURE

        return admin


class Feedback(BaseModel):
    """The feedback class"""

    def __init__(self, admin=None, request=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.request = request
        self.message = message

    def excluded_fields(self):
        return []


class Notification(BaseModel):
    """The notification class"""

    def __init__(self, admin=None, user=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.user = user
        self.message = message
        self.read = False

    def excluded_fields(self):
        return []


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

    def excluded_fields(self):
        return ['updated_at']
