from tests.base_test import BaseTestCase
import json


class SignupTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = {
            "firstname": "Moses",
            "lastname": "Gitau",
            "email": "gitaumoses@gmail.com",
            "username": "gitaumoses",
            "password": "password"
        }

    def test_user_can_sign_up(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 201)  # Resource created

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
