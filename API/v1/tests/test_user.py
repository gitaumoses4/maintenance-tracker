import json

from v1.models import User
from v1.tests.base_test import AuthenticatedTestCase


class UserTestCase(AuthenticatedTestCase):

    def setUp(self):
        super().setUp()
        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"

    def test_get_user_details(self):
        result = self.client().get(self.full_endpoint("users/details"), headers=self.headers)
        self.assertEqual(result.status_code, 200)

        json_result = json.loads(result.get_data(as_text=True))
        self.assertEqual(json_result['status'], "success")

    def tearDown(self):
        super().tearDown()
