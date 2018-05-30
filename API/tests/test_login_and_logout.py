from tests.base_test import BaseTestCase


class LoginTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.admin = {
            "username": "admin",
            "password": "admin"
        }
        self.user = {
            "username": "gitaumoses",
            "password": "andela"
        }

    def test_user_can_login(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().post(self.full_endpoint('users/login'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_admin_can_login(self):
        result = self.client().post(self.full_endpoint('admin/login'), self.admin, self.headers)
        self.assertEqual(result.status_code, 200)

    def test_user_can_logout(self):
        result = self.client().post(self.full_endpoint('users/signup'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 201)

        result = self.client().post(self.full_endpoint('users/login'), data=self.user, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        result = self.client().delete(self.full_endpoint('users/logout'), self.headers)
        self.assertEqual(result.status_code, 200)

    def test_admin_can_logout(self):
        result = self.client().post(self.full_endpoint('admin/login'), data=self.admin, headers=self.headers)
        self.assertEqual(result.status_code, 200)

        result = self.client().delete(self.full_endpoint('admin/logout'), headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        super().tearDown()
