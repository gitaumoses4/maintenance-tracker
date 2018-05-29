from tests.base_test import AuthenticatedTestCase


class FeedbackTestCase(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.feedback = {
            "message": "This is some feedback",
            "request_id": 1
        }

    def test_admin_can_provide_feedback(self):
        result = self.client().post(self.full_endpoint("users/requests/feedback"), self.feedback, self.headers)
        self.assertEqual(result.status_code, 201)

    def test_user_can_get_feedback_for_request(self):
        result = self.client().post(self.full_endpoint("users/requests/feedback"), self.feedback, self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().get(self.full_endpoint("users/requests/1/feedback"))
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        super().tearDown()
