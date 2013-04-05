import os
import unittest
import app
from pymongo import Connection
from mock import patch, Mock


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

    def _mock_requests(self, mock, data):
        m = Mock()
        m.json.return_value = data
        mock.return_value = m

    @patch("requests.get")
    def test_should_receive_facebook_data_and_store_on_database(self, mock):
        data = {"first_name": "First", "last_name": "Last", "email": "first@last.com"}
        self._mock_requests(mock, data)
        request_data = {"access_token": "123awesometoken456"}
        resp = self.api.post("/register/facebook", data=request_data)
        self.assertEqual(201, resp.status_code)
        u = self.db.users.find_one(data)
        self.assertIsNotNone(u)
        self.assertEqual(data["first_name"], u["first_name"])
        self.assertEqual(data["last_name"], u["last_name"])
        self.assertEqual(data["email"], u["email"])
        mock.get.assert_called_once()

    def test_should_return_400_and_do_not_save_user_when_validation_fails(self):
        data = {"access_token": ""}
        resp = self.api.post("/register/facebook", data=data)
        self.assertEqual(400, resp.status_code)
        u = self.db.users.find_one({"first_name": "First"})
        self.assertIsNone(u)


class GithubLoginTestCase(ClientTest, unittest.TestCase):

    pass


class HelperTests(unittest.TestCase):

    def test_has_token_should_check_for_access_token(self):
        is_valid = app.has_token({"access_token": "123token"})
        self.assertTrue(is_valid)

    def test_has_token_should_return_false_when_value_is_empty(self):
        is_valid = app.has_token({"access_token": ""})
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
