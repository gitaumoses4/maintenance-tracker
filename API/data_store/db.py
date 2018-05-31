"""The main data structure"""
from data_store.collections import UserCollection, RequestCollection, FeedbackCollection, NonPersistentCollection
from app.models import Admin


class MaintenanceTrackerDB:
    def __init__(self):
        """Create collections for each model"""
        self.users = UserCollection()
        self.requests = RequestCollection()
        self.feedback = FeedbackCollection()
        self.notifications = NonPersistentCollection()
        self.blacklist = set()
        self.users.insert(Admin.default())

    def clear(self):
        """Clear the data in the collections"""
        self.users.clear()
        self.requests.clear()
        self.feedback.clear()
        self.notifications.clear()

        # Add default admin
        self.users.insert(Admin.default())
