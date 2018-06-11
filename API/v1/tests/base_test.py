import json
from unittest import TestCase
from v1.models import Admin, User

from run import create_app
from v1 import clear


class BaseTestCase(TestCase):
    api_prefix = "/api/v1/"

    def setUp(self):
        self.app = create_app("TESTING")
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.admin_headers = {'Content-Type': 'application/json'}
        self.no_json_headers = {}
        self.admin_no_json_headers = {}

    def full_endpoint(self, path=""):
        return self.api_prefix + path

    def tearDown(self):
        clear()


class AuthenticatedTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        """Create access token for the test cases"""
        self.admin = Admin()
        self.admin.username = "admin"
        self.admin.password = "admin"

        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"

        self.client().post(
            self.full_endpoint("users/signup"),
            data=self.user.to_json_str(False),
            headers=self.headers
        )

        result = self.client().post(
            self.full_endpoint('users/login'),
            data=self.user.to_json_str(False),
            headers=self.headers
        )
        json_result = json.loads(result.get_data(as_text=True))

        self.headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])
        self.no_json_headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])
        # Login admin

        result = self.client().post(
            self.full_endpoint('admin/login'),
            data=self.admin.to_json_str(False),
            headers=self.admin_headers
        )

        json_result = json.loads(result.get_data(as_text=True))
        self.admin_headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])
        self.admin_no_json_headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])

    def tearDown(self):
        super().tearDown()
