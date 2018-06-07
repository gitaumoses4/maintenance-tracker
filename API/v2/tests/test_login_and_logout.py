"""Test case for user and admin login and logout"""
from v2.tests.base_test import BaseTestCase


class LoginTestCase(BaseTestCase):
    """The test case class, for basic authentication testing of the app"""

    def test_user_can_login(self):
        """Signs up user and tests whether the user can login successfully"""
        self.user_signup()
        json_result, status_code = self.user_login()
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_login_without_username(self):
        """Ensures the user cannot login without a username"""
        self.user_signup()
        self.user.username = ""
        json_result, status_code = self.user_login()
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_without_password(self):
        """Ensures the user cannot login without a password"""
        self.user_signup()

        self.user.password = ""
        json_result, status_code = self.user_login()
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_with_unknown_username(self):
        """Ensures the user cannot login without signing up"""
        json_result, status_code = self.user_login()
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_login_with_wrong_password(self):
        """Ensures the user cannot sign in with invalid password"""
        self.user_signup()
        self.user.password = "my_fake_password"
        json_result, status_code = self.user_login()
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_admin_can_login(self):
        """Tests whether the default admin can login successfully"""
        json_result, status_code = self.admin_login()
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_user_can_logout(self):
        """Tests whether a user can logout"""
        self.user_signup()

        json_result, status_code = self.user_login()

        json_result, status_code = self.delete('auth/logout', headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(json_result['data']['token'])
        })
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")
