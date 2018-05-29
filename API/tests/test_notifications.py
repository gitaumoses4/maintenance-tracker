from tests.base_test import AuthenticatedTestCase


class NotificationsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.notification = {
            "user_id": 1,
            "message": "You have a notification"
        }

    def test_can_get_notification_by_id(self):
        result = self.client().post(self.full_endpoint("users/notifications"), self.notification, self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().get(self.full_endpoint("users/notifications/1"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_can_create_notification(self):
        result = self.client().post(self.full_endpoint("users/notifications"), self.notification, self.headers)
        self.assertEqual(result.status_code, 201)

    def test_can_get_all_notifications(self):
        result = self.client().get(self.full_endpoint("users/notifications"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        super().tearDown()
