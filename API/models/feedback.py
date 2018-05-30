from datetime import datetime

from models.base import BaseModel


class Feedback(BaseModel):
    def __init__(self, admin=None, request=None, message="", created_at=datetime.now(), updated_at=datetime.now()):
        super().__init__(created_at, updated_at)
        self.admin = admin
        self.request = request
        self.message = message
