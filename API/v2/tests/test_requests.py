"""Performs the test cases for all the requests"""
import json

from v1.models import Request
from v2.tests.base_test import AuthenticatedTestCase


class RequestsTestCase(AuthenticatedTestCase):
    """The main class to perform the test cases for maintenance/
    repair requests"""

    def setUp(self):
        super().setUp()
        self.request = Request(product_name="Samsung LED",
                               description="Has a broken screen",
                               photo="https://image.ibb.co/mBimvo/Signup.png")

    def create_request(self):
        """Method to create a request"""

        return self.post("users/requests", data=self.request.to_json_str())

    def create_request_and_get_id(self):
        """ Create a request and return the id of the new request"""
        return self.create_request()[0]['data']['request']['id']

    def test_user_can_create_request(self):
        """ Test whether a user can create a request"""
        json_result, status_code = self.create_request()
        self.assertEqual(status_code, 201)

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_create_request_with_invalid_details(self):
        """ This will test that the user cannot create a request with invalid details"""
        self.request.product_name = ""
        json_result, status_code = self.post('users/requests', data=json.dumps({"invalid": "details"}))
        self.assertEqual(status_code, 400)

        self.assertEqual(json_result['status'], "error")

    def test_user_can_get_all_requests(self):
        """This will test whether a user can get all their requests"""
        json_result, status_code = self.get("users/requests")
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_admin_can_get_all_requests(self):
        """This will tests whether the admin can get the requests in the system"""
        json_result, status_code = self.get("requests")
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_user_cannot_modify_request_with_invalid_details(self):
        """Ensures a user cannot modify a request with invalid details"""
        request_id = self.create_request_and_get_id()

        json_result, status_code = self.put("users/requests/{}".format(request_id),
                                            data=json.dumps({"invalid": "details"}))
        print(json_result)
        self.assertEqual(status_code, 400)
        self.assertEqual(json_result['status'], "error")

    def test_user_can_modify_request(self):
        """Ensures a user can modify a request"""
        request_id = self.create_request_and_get_id()

        self.request.description = "Some New Description"
        self.put("users/requests/{}".format(request_id), data=self.request.to_json_str(False))

        json_result, status_code = self.get("users/requests/{}".format(request_id),
                                            )
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")
        self.assertEqual(json_result['data']['request']['description'], "Some New Description")

    def test_admin_can_approve_request(self):
        """Checks whether an admin can approve a request"""
        request_id = self.create_request_and_get_id()

        json_result, status_code = self.put("requests/{}/approve".format(request_id),
                                            headers=self.admin_headers)

        self.assertEqual(status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_disapprove_request(self):
        """Ensures an admin can disapprove a request"""
        request_id = self.create_request_and_get_id()
        json_result, status_code = self.put("requests/{}/disapprove".format(request_id),
                                            headers=self.admin_headers)
        self.assertEqual(status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_admin_can_resolve_request(self):
        """Ensures an admin can resolve a request"""
        request_id = self.create_request_and_get_id()

        json_result, status_code = self.put("requests/{}/resolve".format(request_id),
                                            headers=self.admin_headers)

        self.assertEqual(status_code, 200)
        self.assertEqual(json_result['status'], "success")

    def test_can_only_approved_pending_request(self):
        """Ensures the admin can only approve a pending request"""
        request_id = self.create_request_and_get_id()
        self.put("requests/{}/approve".format(request_id))

        json_result, status_code = self.put("requests/{}/approve".format(request_id))
        self.assertEqual(status_code, 400)
        self.assertEqual(json_result['status'], "error")

    def test_can_get_request_by_id(self):
        """Checks whether a user can get a request by it's id"""
        request_id = self.create_request_and_get_id()
        json_result, status_code = self.get("users/requests/{}".format(request_id))
        self.assertEqual(status_code, 200)

        self.assertEqual(json_result['status'], "success")

    def test_cannot_get_request_with_unknown_id(self):
        """Checks whether a user can get a request with unknown id"""
        json_result, status_code = self.get("users/requests/{}".format(123123),
                                            )
        self.assertEqual(status_code, 404)

        self.assertEqual(json_result['status'], "error")

    def test_user_cannot_modify_request_not_created_by_them(self):
        """Ensures a user cannot modify a request not created by them"""
        request_id = self.create_request_and_get_id()
        # Login as different user
        self.user.username = "FakeUsername"
        self.user.email = "fakeemail@fakeemails.fake"
        self.user_signup()

        json_result, status_code = self.user_login()

        self.headers['Authorization'] = 'Bearer {}'.format(json_result['data']['token'])

        json_result, status_code = self.get("users/requests/{}".format(request_id))
        self.assertEqual(status_code, 401)
        self.assertEqual(json_result['status'], "error")
