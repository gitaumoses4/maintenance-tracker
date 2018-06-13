"""Test case for notification endpoints"""
import json

from v1.models import Notification
from v2.tests.base_test import AuthenticatedTestCase


class NotificationsTestCase(AuthenticatedTestCase):
    """The main class to test for notification endpoints"""

    def setUp(self):
        super().setUp()
        self.notification = Notification(message="You have a notification")
        json_result = self.get("users/details", headers=self.headers)[0]
        self.user.id = json_result['data']['user']['id']

    def create_notification(self):
        """Creates a notification and returns the response"""
        return self.post("notifications/{}".format(self.user.id),
                         data=self.notification.to_json_str(),
                         headers=self.admin_headers)

    def create_notification_and_get_id(self):
        """Returns the id of the created notification"""
        return self.create_notification()[0]['data']['notification']['id']

    def test_cannot_get_notification_that_does_not_exist(self):
        """Ensures cannot get notification that does not exist"""
        json_result, status_code = self.get("users/notifications/{}".format(223423))
        self.assertEqual(status_code, 404)

        self.assertEqual(json_result['status'], "error")

    def test_can_get_notification_by_id(self):
        """Tests whether user can get a notification by id"""
        notification_id = self.create_notification_and_get_id()

        json_result, status_code = self.get("users/notifications/{}".format(notification_id))
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_can_create_notification(self):
        """Tests whether an admin can send a notification"""
        json_result, status_code = self.create_notification()

        self.assertEqual(status_code, 201)
        self.assertEqual(json_result['status'], "success")

    def test_cannot_create_notification_for_non_existing_user(self):
        """Checks to see that an admin cannot send notification to non-existing users"""
        json_result, status_code = self.post("notifications/{}".format(123123),
                                             data=self.notification.to_json_str(),
                                             headers=self.admin_headers)

        self.assertEqual(status_code, 404)
        self.assertEqual(json_result['status'], "error")

    def test_cannot_create_notification_with_empty_message(self):
        """Ensures the admin cannot create notification with an empty message"""
        json_result, status_code = self.post("notifications/{}".format(self.user.id),
                                             data=json.dumps({"fake": ""}),
                                             headers=self.admin_headers)

        self.assertEqual(status_code, 400)
        self.assertEqual(json_result['status'], "error")

    def test_can_get_all_notifications(self):
        """Tests whether user can get all their notifications"""
        self.create_notification()

        json_result, status_code = self.get("users/notifications/all")
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_can_get_read_notifications(self):
        """Tests whether user can get all their read notifications"""
        self.create_notification()

        json_result, status_code = self.get("users/notifications/read")
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_can_get_unread_notifications(self):
        """Tests whether user can get all their unread notifications"""
        self.create_notification()

        json_result, status_code = self.get("users/notifications/unread")
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_can_mark_notification_as_read(self):
        """Tests whether a notification can be marked as read"""
        notification_id = self.create_notification_and_get_id()

        json_result, status_code = self.put("users/notifications/{}".format(notification_id))

        self.assertEqual(status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_cannot_mark_non_existing_notification_as_read(self):
        """Checks whether a non-existing notification can be marked as read"""
        json_result, status_code = self.put("users/notifications/{}".format(123123))

        self.assertEqual(status_code, 404)
        self.assertEqual(json_result['status'], "error")
