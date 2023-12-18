import unittest

from run import create_app
from v1.tests.base_test import BaseTestCase, AuthenticatedTestCase


class DocsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app("TESTING")
        self.client = self.app.test_client

    def test_docs_index_page(self):
        result = self.client().get("/")

        self.assertIsNotNone(result)
