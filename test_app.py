import unittest
from app import app


class ClientTest(object):

    @classmethod
    def setUpClass(self):
        self.api = app.test_client()


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

    def test_should_receive_facebook_data_and_store_on_database(self):
        resp = self.api.post("/facebook-login")
        self.assertEqual(201, resp.status_code)

if __name__ == "__main__":
    unittest.main()
