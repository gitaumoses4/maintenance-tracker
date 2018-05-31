from tests.base_test import BaseTestCase
import json
from app.models import Admin, User


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.admin = Admin()
        self.admin.username = "admin"
        self.admin.password = "admin"

        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"

    def test_user_can_login(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('users/login'), data=self.user.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_login(self):
        result = self.client().post(self.full_endpoint('admin/login'), data=self.admin.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_logout(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('users/login'), data=self.user.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().delete(self.full_endpoint('users/logout'), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(json_result['data']['token'])
        })
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_logout(self):
        result = self.client().post(self.full_endpoint('admin/login'), data=self.admin.to_json_str(),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().delete(self.full_endpoint('admin/logout'), headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(json_result['data']['token'])
        })
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
