"""Contains tests for user sign up"""
from v2.tests.base_test import BaseTestCase


class SignupTestCase(BaseTestCase):
    """The main class to test for sign up of the user"""

    def test_user_can_sign_up(self):
        """Tests whether a user can sign up successfully"""
        json_result, status_code = self.user_signup()
        self.assertEqual(status_code, 201)  # Resource created

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_sign_up_with_invalid_details(self):
        """Tests whether a user can sign up with invalid details"""
        self.user.username = ""
        json_result, status_code = self.user_signup()
        self.assertEqual(status_code, 400)  # Resource created

        self.assertEqual(json_result['status'], "error")
