""" Default testing cases for the API"""
import json
from unittest import TestCase

from migrate import Migration
from v1.models import Admin, User

from run import create_app


class BaseTestCase(TestCase):
    """This base test class contains the required methods and functions
    to make API test calls """

    api_prefix = "/api/v2/"

    def setUp(self):
        self.app = create_app("TESTING")
        self.migration = Migration()
        self.migration.set_up()
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}
        self.admin_headers = {'Content-Type': 'application/json'}

        self.user = User()
        self.user.firstname = "Moses"
        self.user.lastname = "Gitau"
        self.user.username = "gitaumoses"
        self.user.email = "gitaumoses@gmail.com"
        self.user.password = "password"

        self.admin = Admin()
        self.admin.username = "admin"
        self.admin.password = "admin"

    def full_endpoint(self, path=""):
        """ Appends the API prefix to the requested endpoint"""
        return self.api_prefix + path

    def user_login(self, user=None):
        """ Call this method from child classes to request user login """
        if user is None:
            user = self.user
        return self.post("auth/login", user.to_json_str(False), self.headers)

    def user_signup(self, user=None):
        """ Method to perform the API call to sign up a user"""
        if user is None:
            user = self.user
        return self.post("auth/signup", user.to_json_str(False), self.headers)

    def admin_login(self):
        """ Method to perform the API call to login the default admin"""
        return self.post("auth/login", self.admin.to_json_str(False), self.headers)

    def post(self, endpoint="", data="", headers=None):
        """ Make API calls for the POST method"""
        if headers is None:
            headers = self.headers
        return self.make_api_call("POST", endpoint, data, headers)

    def put(self, endpoint="", data="", headers=None):
        """ Make API calls for the PUT method"""
        if headers is None:
            headers = self.headers
        return self.make_api_call("PUT", endpoint, data, headers)

    def get(self, endpoint="", data="", headers=None):
        """ Make API calls for the GET method"""
        if headers is None:
            headers = self.headers
        return self.make_api_call("GET", endpoint, data, headers)

    def delete(self, endpoint="", data="", headers=None):
        """ Make API calls for the DELETE method

        :param endpoint:
        :param data:
        :param headers:
        """
        if headers is None:
            headers = self.headers
        return self.make_api_call("DELETE", endpoint, data, headers)

    def make_api_call(self, method="GET", endpoint="", data="", headers=None):
        """ Makes API calls and returns the JSON result and the response code"""
        endpoint = self.full_endpoint(endpoint)
        if method == "GET":
            result = self.client().get(endpoint, data=data, headers=headers)
        elif method == "POST":
            result = self.client().post(endpoint, data=data, headers=headers)
        elif method == "PUT":
            result = self.client().put(endpoint, data=data, headers=headers)
        elif method == "DELETE":
            result = self.client().delete(endpoint, data=data, headers=headers)
        else:
            result = None
        if result is not None:
            json_result = json.loads(result.get_data(as_text=True))
            return json_result, result.status_code
        return None

    def tearDown(self):
        self.migration.tear_down()


class AuthenticatedTestCase(BaseTestCase):
    """This implements a test case with the requirement of authenticated."""

    def setUp(self):
        super().setUp()
        self.user_signup()
        json_result = self.user_login()[0]

        self.headers['Authorization'] = 'Bearer {}'.format(
            json_result['data']['token'])
        # Login admin

        json_result = self.admin_login()[0]

        self.admin_headers['Authorization'] = 'Bearer {}'.format(
            json_result['data']['token'])

    def test_admin_endpoints(self):
        """Checks whether the admin endpoints are guarded from other users"""
        endpoints = {
            "POST": ['requests/1/feedback', "notifications/1"],
            "GET": ["requests"],
            "PUT": ["requests/1/approve", "requests/1/disapprove", "requests/1/resolve", "users/1/upgrade"],
            "DELETE": []
        }
        self.endpoints_check(endpoints, headers=self.headers, message="User not an Admin", expected_status_code=401)

    def test_user_endpoints_request_in_json(self):
        """Tests for the endpoints that allow only a json body"""

        user_endpoints = {
            "POST": ["auth/signup", "auth/login", "users/requests"],
            "PUT": ["users/requests/1"],
            "GET": [],
            "DELETE": []
        }
        admin_endpoints = {
            "POST": ["requests/1/feedback", "notifications/1"],
            "GET": [],
            "PUT": [],
            "DELETE": []
        }

        headers = self.headers.copy()
        del headers['Content-Type']

        admin_headers = self.admin_headers.copy()
        del admin_headers['Content-Type']

        self.endpoints_check(user_endpoints, headers=headers, message="Request should be in JSON")
        self.endpoints_check(
            admin_endpoints, headers=admin_headers, message="Request should be in JSON")

    def endpoints_check(self, endpoints, body="", headers=None, message="", expected_status_code=400):
        """ Tests that the specified endpoints meet a particular response message

        :param expected_status_code:
        :param body:
        :param message:
        :param headers:
        :param endpoints:
        """
        for method in endpoints:
            for endpoint in endpoints[method]:
                json_result, status_code = self.make_api_call(
                    method, endpoint, body, headers)
                self.assertEqual(status_code, expected_status_code)
                self.assertEqual(
                    json_result['message'], message)
