from datetime import datetime

from models.base import BaseModel


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