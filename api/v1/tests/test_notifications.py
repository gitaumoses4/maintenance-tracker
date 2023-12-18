import json

from v1.models import Notification
from v1.tests.base_test import AuthenticatedTestCase


class NotificationsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.notification = Notification(message="You have a notification")
        result = self.client().get(self.full_endpoint("users/details"), headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.user.id = json_result['data']['user']['id']

    def test_cannot_get_notification_that_does_not_exist(self):
        result = self.client().get(
            self.full_endpoint("users/notifications/{}".format(223423)),
            headers=self.headers)
        self.assertEqual(result.status_code, 404)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_can_get_notification_by_id(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(False),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

        notification_id = json_result['data']['notification']['id']
        result = self.client().get(
            self.full_endpoint("users/notifications/{}".format(notification_id)),
            headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_can_create_notification(self):
        result = self.client().post(self.full_endpoint('admin/users/{}/notifications'.format(self.user.id))
                                    , headers=self.admin_no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['message'], "Request should be in JSON")

        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(False),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

    def test_cannot_create_notification_for_non_existing_user(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(123123)),
            data=self.notification.to_json_str(False),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 404)
        self.assertEqual(json_result['status'], "error")

    def test_cannot_create_notification_with_empty_message(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=json.dumps({"fake": ""}),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 400)
        self.assertEqual(json_result['status'], "error")

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

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_can_mark_notification_as_read(self):
        result = self.client().post(
            self.full_endpoint("admin/users/{}/notifications".format(self.user.id)),
            data=self.notification.to_json_str(),
            headers=self.admin_headers)

        json_result = json.loads(result.get_data(as_text=True))

        self.assertEqual(result.status_code, 201)
        self.assertEqual(json_result['status'], "success")

        notification_id = json_result['data']['notification']['id']

        result = self.client().put(
            self.full_endpoint("users/notifications/{}".format(notification_id)),
            headers=self.headers)

        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_cannot_mark_non_existing_notification_as_read(self):
        result = self.client().put(
            self.full_endpoint("users/notifications/{}".format(123123)),
            headers=self.headers)

        self.assertEqual(result.status_code, 404)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()
