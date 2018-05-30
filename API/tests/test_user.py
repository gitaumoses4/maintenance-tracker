from tests.base_test import AuthenticatedTestCase


class UserTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.user = {
            "username": "gitaumoses",
            "password": "andela"
        }

    def test_get_user_details(self):
        result = self.client().post(self.full_endpoint("users/login"), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        result = self.client().get(self.full_endpoint("users/details"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        super().tearDown()
