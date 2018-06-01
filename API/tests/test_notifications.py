import json

from app.models import Notification
from tests.base_test import AuthenticatedTestCase


class NotificationsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.notification = Notification(message="You have a notification")
        result = self.client().get(self.full_endpoint("users/details"), headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.user.id = json_result['data']['user']['id']

    def test_can_get_notification_by_id(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(False),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(
            self.full_endpoint("users/notifications/{}".format(json_result['data']['notification']['id'])),
            headers=self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_can_create_notification(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(False),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

    def test_can_get_all_notifications(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(self.full_endpoint("users/notifications"), headers=self.headers)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_can_mark_notification_as_read(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

        result = self.client().put(
            self.full_endpoint("users/notifications/{}".format(json_result['data']['notification']['id'])),
            headers=self.headers)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
