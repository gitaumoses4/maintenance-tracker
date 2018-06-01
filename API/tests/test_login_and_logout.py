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

    def sign_up(self):
        return self.client().post(self.full_endpoint('users/signup'), data=self.user.to_json_str(False),
                                  headers=self.headers)

    def user_login(self):
        return self.client().post(self.full_endpoint('users/login'), data=self.user.to_json_str(False),
                                  headers=self.headers)

    def admin_login(self):
        return self.client().post(self.full_endpoint('admin/login'), data=self.admin.to_json_str(False),
                                  headers=self.headers)

    def test_user_cannot_login_as_admin(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('admin/login'), data=self.user.to_json_str(False),
                                    headers=self.headers)
        self.assertEqual(result.status_code, 401)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_can_login(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.client().post(self.full_endpoint('users/login'),
                                    headers=self.no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['message'], "Request should be in JSON")

        result = self.user_login()
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_login_without_username(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.user.username = ""
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_without_password(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.user.password = ""
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_with_unknown_username(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.user.username = "my_fake_username"
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_with_wrong_password(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        self.user.password = "my_fake_password"
        result = self.user_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_can_login(self):
        result = self.client().post(self.full_endpoint('admin/login'),
                                    headers=self.admin_no_json_headers)
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['message'], "Request should be in JSON")

        result = self.admin_login()
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def test_user_can_logout(self):
        result = self.sign_up()
        self.assertEqual(result.status_code, 201)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

        result = self.user_login()
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
        result = self.admin_login()
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

    def test_admin_cannot_login_without_username(self):
        self.admin.username = ""
        result = self.admin_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_login_without_password(self):
        self.admin.password = ""
        result = self.admin_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_login_with_unknown_username(self):
        self.admin.username = "my_fake_username"
        result = self.admin_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def test_admin_cannot_login_with_wrong_password(self):
        self.admin.password = "wrong_password"
        result = self.admin_login()
        self.assertEqual(result.status_code, 400)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "error")

    def tearDown(self):
        super().tearDown()
