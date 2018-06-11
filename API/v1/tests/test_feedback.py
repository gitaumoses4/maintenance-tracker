import json

from v1.models import Feedback, Request
from v1.tests.base_test import AuthenticatedTestCase
import unittest


class FeedbackTestCase(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen")
        self.feedback = Feedback(message="This is some feedback")

    def test_admin_cannot_provide_feedback_for_non_existing_request(self):
        request_id = 123123
        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(request_id)),
            data=self.feedback.to_json_str(False),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 404)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_provide_feedback_with_invalid_details(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(False),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.feedback.message = ""
        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(json_result['data']['request']['id'])),
            data=self.feedback.to_json_str(False),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_can_provide_feedback(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(False),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        request_id = json_result['data']['request']['id']
        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(request_id)),
            headers=self.admin_no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['message'], "Request should be in JSON")

        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(request_id)),
            data=self.feedback.to_json_str(False),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_get_feedback_for_request(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(False),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        request_id = json_result['data']['request']['id']
        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(request_id)),
            data=self.feedback.to_json_str(False),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(
            self.full_endpoint("users/requests/{}/feedback".format(request_id)),
            headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_get_feedback_for_non_existing_request(self):
        request_id = 123123
        result = self.client().get(
            self.full_endpoint("users/requests/{}/feedback".format(request_id)),
            headers=self.headers)
        self.assertEqual(result.status_code, 404)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_get_feedback_not_meant_for_them(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(False),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")
        request_id = json_result['data']['request']['id']

        # Create request
        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(request_id)),
            data=self.feedback.to_json_str(False),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 201)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        # Login as different user
        self.user.username = "FakeUsername"
        self.user.email = "fakeemail@fakeemails.fake"
        self.client().post(
            self.full_endpoint("users/signup"),
            data=self.user.to_json_str(False),
            headers=self.headers
        )
        result = self.client().post(
            self.full_endpoint('users/login'),
            data=self.user.to_json_str(False),
            headers=self.headers
        )
        json_result = json.loads(result.get_data(as_text=True))

        self.headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])

        result = self.client().get(
            self.full_endpoint("users/requests/{}/feedback".format(request_id)),
            headers=self.headers)
        self.assertEqual(result.status_code, 401)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
