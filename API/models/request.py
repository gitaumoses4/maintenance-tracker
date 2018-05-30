from datetime import datetime

from models.base import BaseModel


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
