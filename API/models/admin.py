import os
from datetime import datetime

from models.user import User


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
        admin.username = os.getenv("DEFAULT_ADMIN_USER_NAME")
        admin.password = os.getenv("DEFAULT_ADMIN_PASSWORD")
        admin.profile_picture = os.getenv("DEFAULT_ADMIN_PROFILE_PICTURE")

        return admin