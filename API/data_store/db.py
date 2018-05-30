from data_store.collections import UserCollection, RequestCollection, FeedbackCollection, NonPersistentCollection
from models.admin import Admin


class MaintenanceTrackerDB:
    def __init__(self):
        self.users = UserCollection()
        self.requests = RequestCollection()
        self.feedback = FeedbackCollection()
        self.notifications = NonPersistentCollection()
        self.blacklist = set()

    def clear(self):
        self.users.clear()
        self.requests.clear()
        self.feedback.clear()
        self.notifications.clear()

        # Add default admin
        self.users.insert(Admin.default())