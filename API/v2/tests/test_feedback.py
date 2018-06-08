"""Provides the functionality to test for the ability to provide and receive feedback"""
import json

from v1.models import Feedback, Request
from v2.tests.base_test import AuthenticatedTestCase


class FeedbackTestCase(AuthenticatedTestCase):
    """Class to test for feedback endpoints"""

    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen")

        self.feedback = Feedback(message="This is some feedback")

    def create_request(self):
        """Creates a request which will be provided feedback for"""
        return self.post("users/requests", self.request.to_json_str())[0]['data']['request']['id']

    def create_feedback_for_request(self):
        """Creates a request and provides feedback"""
        request_id = self.create_request()
        self.request.id = request_id

        return self.post("requests/{}/feedback".format(request_id), self.feedback.to_json_str(),
                         self.admin_headers)

    def test_admin_cannot_provide_feedback_for_non_existing_request(self):
        """Tests whether the admin can provide feedback for a user that does not exist in the database"""
        json_result, status_code = self.post("requests/123123/feedback", self.feedback.to_json_str(),
                                             self.admin_headers)

        self.assertEqual(status_code, 404)

        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_provide_feedback_with_invalid_details(self):
        """Tests whether the admin can provide feedback with invalid details"""
        request_id = self.create_request()

        json_result, status_code = self.post("requests/{}/feedback".format(request_id),
                                             data=json.dumps({"Invalid": "Details"}),
                                             headers=self.admin_headers)
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_admin_can_provide_feedback(self):
        """Tests whether the admin can provide feedback to requests"""
        json_result, status_code = self.create_feedback_for_request()
        self.assertEqual(status_code, 201)

        self.assertEqual(json_result['status'], "success")

    def test_user_can_get_feedback_for_request(self):
        """Tests whether the user can get feedback for a particular request"""
        self.create_feedback_for_request()

        json_result, status_code = self.get("users/requests/{}/feedback".format(self.request.id),
                                            headers=self.headers)
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_get_feedback_for_non_existing_request(self):
        """Ensures a user cannot get feedback for a non-existing request"""
        request_id = 123123
        json_result, status_code = self.get(
            self.full_endpoint("users/requests/{}/feedback".format(request_id)),
            headers=self.headers)
        self.assertEqual(status_code, 404)

        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_get_feedback_not_meant_for_them(self):
        """Ensures a user cannot get feedback meant for a request not created by them"""
        self.create_feedback_for_request()

        # Login as different user
        self.user.username = "FakeUsername"
        self.user.email = "fakeemail@fakeemails.fake"
        self.user_signup()
        json_result, status_code = self.user_login()

        self.headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])

        json_result, status_code = self.get("users/requests/{}/feedback".format(self.request.id),
                                            headers=self.headers)
        self.assertEqual(status_code, 401)

        self.assertEqual(json_result['status'], "error")
