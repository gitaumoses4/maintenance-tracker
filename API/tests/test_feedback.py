import json

from models.feedback import Feedback
from models.request import Request
from tests.base_test import AuthenticatedTestCase
import unittest


class FeedbackTestCase(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen")
        self.feedback = Feedback(message="This is some feedback")

    def test_admin_can_provide_feedback(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(json_result['data']['request']['id'])),
            data=self.feedback.to_json_str(),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_get_feedback_for_request(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(
            self.full_endpoint("admin/requests/{}/feedback".format(json_result['data']['request']['id'])),
            data=self.feedback.to_json_str(),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(
            self.full_endpoint("users/requests/{}/feedback".format(json_result['data']['request']['id'])),
            headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()


if __name__ == '__main__':
    unittest.main()
