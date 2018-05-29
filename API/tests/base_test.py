from unittest import TestCase
from app import initialize_app


class BaseTestCase(TestCase):
    api_prefix = "/api/v1/"

    def setUp(self):
        self.app = initialize_app("TESTING")
        self.client = self.app.test_client
        self.headers = {'Content-Type': 'application/json'}

    def full_endpoint(self, path=""):
        return self.api_prefix + path


class AuthenticatedTestCase(BaseTestCase):

    def setUp(self):
        """Create access token for the test cases"""

    def tearDown(self):
        pass
