from tests.base_test import BaseTestCase
from app.models import User
import json


class SignupTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"

    def test_user_can_sign_up(self):
        result = self.client().post(self.full_endpoint('users/signup'), headers=self.no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['message'], "Request should be in JSON")

        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                    headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 201)  # Resource created

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_sign_up_with_invalid_details(self):
        self.user.username = ""
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                    headers=self.headers)
        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(result.status_code, 400)  # Resource created

        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()
