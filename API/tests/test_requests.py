import json

from app.models import Request
from tests.base_test import AuthenticatedTestCase


class RequestsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen",
                               photo="https://image.ibb.co/mBimvo/Signup.png")

    def create_request(self):
        return self.client().post(self.full_endpoint("users/requests"),
                                  data=self.request.to_json_str(False),
                                  headers=self.headers)

    def test_user_can_create_request(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_create_request_with_invalid_details(self):
        self.request.product_name = ""
        result = self.create_request()
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_can_get_all_requests(self):
        result = self.client().get(self.full_endpoint("users/requests"),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_get_all_requests(self):
        result = self.client().get(self.full_endpoint("admin/requests"),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_modify_request_with_invalid_details(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.request.description = None
        result = self.client().put(self.full_endpoint("users/requests/{}".format(json_result['data']['request']['id'])),
                                   data=json.dumps({"invalid": "details"}),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_can_modify_request(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.request.description = "Some New Description"
        result = self.client().put(self.full_endpoint("users/requests/{}".format(json_result['data']['request']['id'])),
                                   data=self.request.to_json_str(False),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(self.full_endpoint("users/requests/{}".format(json_result['data']['request']['id'])),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")
        self.assertEqual(json_result['data']['request']['description'], "Some New Description")

    def test_admin_can_modify_request(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().put(
            self.full_endpoint("admin/requests/{}".format(json_result['data']['request']['id'])),
            data=json.dumps({"status": "Approved"}),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_cannot_modify_non_existing_request(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().put(
            self.full_endpoint("admin/requests/{}".format(12323)),
            data=json.dumps({"status": "Approved"}),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 404)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_modify_request_without_status(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().put(
            self.full_endpoint("admin/requests/{}".format(json_result['data']['request']['id'])),
            data=json.dumps({"none": "none"}),
            headers=self.admin_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_can_get_request_by_id(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().get(self.full_endpoint("users/requests/{}".format(json_result['data']['request']['id'])),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_cannot_get_request_with_unknown_id(self):
        result = self.client().get(self.full_endpoint("users/requests/{}".format(123123)),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 404)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_modify_request_not_created_by_them(self):
        result = self.create_request()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))

        request_id = json_result['data']['request']['id']
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

        result = self.client().get(self.full_endpoint("users/requests/{}".format(request_id)),
                                   headers=self.headers)
        self.assertEqual(result.status_code, 401)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()
