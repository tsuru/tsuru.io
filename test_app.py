import unittest
from app import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.api = app.test_client()

    def test_should_get_index_and_be_success(self):
        resp = self.api.get("/")
        self.assertEqual(200, resp.status_code)

    def test_should_get_confirmation_and_be_success(self):
        resp = self.api.get("/confirmation")
        self.assertEqual(200, resp.status_code)

    def test_should_have_facebook_login_button_in_content(self):
        resp = self.api.get("/")
        self.assertIn("facebook-login", resp.data)


if __name__ == "__main__":
    unittest.main()
