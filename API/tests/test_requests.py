from tests.base_test import AuthenticatedTestCase


class RequestsTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.request = {
            "product_name": "Samsung LED TV",
            "description": "The screen has a crack",
            "status": "pending",
            "photo": "",
            "user_id": 1
        }

    def test_user_can_create_request(self):
        result = self.client().post(self.full_endpoint("users/requests"), data=self.request, headers=self.headers)
        self.assertEqual(result.status_code, 201)

    def test_can_get_all_requests(self):
        result = self.client().get(self.full_endpoint("users/requests"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_user_can_modify_request(self):
        result = self.client().post(self.full_endpoint("users/requests"), data=self.request, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().patch(self.full_endpoint("users/requests/1"), data=self.request, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        result = self.client().get(self.full_endpoint("users/requests/1"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_admin_can_modify_request(self):
        result = self.client().patch(self.full_endpoint("users/requests/1"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_can_get_request_by_id(self):
        result = self.client().post(self.full_endpoint("users/requests"), data=self.request, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().get(self.full_endpoint("users/requests/1"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        super().tearDown()
