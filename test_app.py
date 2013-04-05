import os
import unittest
import app
from pymongo import Connection


class ClientTest(object):

    @classmethod
    def setUpClass(self):
        self.api = app.app.test_client()


class AppTestCase(ClientTest, unittest.TestCase):

    def test_should_get_index_and_be_success(self):
        resp = self.api.get("/")
        self.assertEqual(200, resp.status_code)

    def test_should_get_confirmation_and_be_success(self):
        resp = self.api.get("/confirmation")
        self.assertEqual(200, resp.status_code)

    def test_should_have_facebook_login_button_in_content(self):
        resp = self.api.get("/")
        self.assertIn("facebook-login", resp.data)


class FacebookLoginTestCase(ClientTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_uri_port = app.MONGO_URI.split(":")
        host = mongo_uri_port[0]
        port = int(mongo_uri_port[1])
        cls.conn = Connection(host, port)
        cls.db = cls.conn[app.MONGO_DATABASE_NAME]
        ClientTest.setUpClass()

    def tearDown(self):
        self.db.users.remove()

    def test_should_receive_facebook_data_and_store_on_database(self):
        data = {"first_name": "First", "last_name": "Last"}
        resp = self.api.post("/login/facebook", data=data)
        self.assertEqual(201, resp.status_code)
        u = self.db.users.find_one({"first_name": "First", "last_name": "Last"})
        self.assertIsNotNone(u)
        expected = {"first_name": "First", "last_name": "Last"}
        self.assertEqual(expected["first_name"], u["first_name"])
        self.assertEqual(expected["last_name"], u["last_name"])

    def test_should_return_400_and_do_not_save_user_when_validation_fails(self):
        data = {"first_name": "First", "last_name": ""}
        resp = self.api.post("/login/facebook", data=data)
        self.assertEqual(400, resp.status_code)
        u = self.db.users.find_one({"first_name": "First"})
        self.assertIsNone(u)


class GithubLoginTestCase(ClientTest, unittest.TestCase):

    pass


class HelperTests(unittest.TestCase):

    def test_is_login_valid_should_check_for_first_name_and_last_name(self):
        is_valid = app.is_login_valid({"first_name": "First", "last_name": "Last"})
        self.assertTrue(is_valid)

    def test_valida_login_should_return_false_when_there_is_no_last_name(self):
        is_valid = app.is_login_valid({"first_name": "First"})
        self.assertFalse(is_valid)

    def test_valid_login_should_return_false_when_one_value_is_empty(self):
        is_valid = app.is_login_valid({"first_name": "First", "last_name": ""})
        self.assertFalse(is_valid)
        is_valid = app.is_login_valid({"first_name": "", "last_name": "Last"})
        self.assertFalse(is_valid)

if __name__ == "__main__":
    unittest.main()
