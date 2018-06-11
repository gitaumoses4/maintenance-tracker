"""Test for user functions such as getting their details and upgrading to an admin"""
from v2.tests.base_test import AuthenticatedTestCase


class UserTestCase(AuthenticatedTestCase):
    """The main class to perform user functions check it extends AuthenticatedTestCase to ensure
    the user is logged in first"""

    def test_get_user_details(self):
        """Checks whether a logged in user can get their details"""
        json_result, status_code = self.get("users/details", headers=self.headers)
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_admin_can_upgrade_user(self):
        """Logs in the admin and checks to see whether the user can be upgraded"""
        json_result = self.get("users/details", headers=self.headers)[0]
        self.user.id = json_result['data']['user']['id']

        json_result, status_code = self.put("users/{}/upgrade".format(self.user.id), headers=self.admin_headers)
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")
