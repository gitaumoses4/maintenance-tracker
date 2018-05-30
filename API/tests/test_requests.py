import json

from models.request import Request
from tests.base_test import AuthenticatedTestCase


class RequestsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen")

    def test_user_can_create_request(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_can_get_all_requests(self):
        result = self.client().get(self.full_endpoint("users/requests"),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_modify_request(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().put(self.full_endpoint("users/requests/1"),
                                   data=self.request.to_json_str(),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(self.full_endpoint("users/requests/1"),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_modify_request(self):
        result = self.client().patch(self.full_endpoint("admin/requests/1"),
                                     headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_can_get_request_by_id(self):
        result = self.client().post(self.full_endpoint("users/requests"),
                                    data=self.request.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(self.full_endpoint("users/requests/1"),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
