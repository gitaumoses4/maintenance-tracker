from tests.base_test import BaseTestCase


class SignupTestCase(BaseTestCase):
    def setUp(self):
        self.user = {
            "firstname": "Moses",
            "lastname": "Gitau",
            "email": "gitaumoses4@gmail.com",
            "username": "gitaumoses4",
            "password": "andela"
        }
        super().setUp()

    def test_user_can_sign_up(self):
        result = self.client().post(self.full_endpoint('user/signup'), self.user, self.headers)
        self.assertEqual(result.status_code, 201)  # Resource created

    def tearDown(self):
        super().tearDown()
