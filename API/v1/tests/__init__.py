import unittest

from app import initialize_app
from tests.base_test import BaseTestCase, AuthenticatedTestCase


class DocsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = initialize_app("TESTING")
        self.client = self.app.test_client

    def test_docs_index_page(self):
        result = self.client().get("/")

        self.assertIsNotNone(result)
