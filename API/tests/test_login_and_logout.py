from tests.base_test import BaseTestCase
import json


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.admin = {
            "username": "admin",
            "password": "admin"
        }
        self.user = {
            "firstname": "Moses",
            "lastname": "Gitau",
            "email": "gitaumoses@gmail.com",
            "username": "gitaumoses",
            "password": "password"
        }

    def test_user_can_login(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('users/login'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_login(self):
        result = self.client().post(self.full_endpoint('admin/login'), self.admin, self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_logout(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('users/login'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().delete(self.full_endpoint('users/logout'), self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_logout(self):
        result = self.client().post(self.full_endpoint('admin/login'), data=self.admin, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().delete(self.full_endpoint('admin/logout'), headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_test=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
