""" Tests for web routes, checks whether the API home displays docs"""
import unittest

from run import create_app
from v2.tests.base_test import BaseTestCase, AuthenticatedTestCase


class DocsTestCase(unittest.TestCase):
    """Class to test for the documentations view"""

    def setUp(self):
        self.app = create_app("TESTING")
        self.client = self.app.test_client

    def test_docs_index_page(self):
        """Test for the docs page"""
        result = self.client().get("/")

        self.assertIsNotNone(result)
