from datetime import datetime

from models.base import BaseModel


class Notification(BaseModel):
    def __init__(self, admin=None, user=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.user = user
        self.message = message
        self.read = False
