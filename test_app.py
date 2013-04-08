import hashlib
import unittest

import werkzeug
from pymongo import Connection
from mock import patch, Mock

import app


class ClientTest(object):

    @classmethod
    def setUpClass(self):
        app.app.config["CSRF_ENABLED"] = False
        self.api = app.app.test_client()


class DatabaseTest(object):

    @classmethod
    def setUpClass(cls):
        mongo_uri_port = app.MONGO_URI.split(":")
        host = mongo_uri_port[0]
        port = int(mongo_uri_port[1])
        cls.conn = Connection(host, port)
        cls.db = cls.conn[app.MONGO_DATABASE_NAME]

    @classmethod
    def tearDownClass(cls):
        cls.conn.drop_database(app.MONGO_DATABASE_NAME)


class AppTestCase(ClientTest, unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        app.SIGN_KEY = None

    def test_should_get_index_and_be_success(self):
        resp = self.api.get("/")
        self.assertEqual(200, resp.status_code)

    @patch("flask.render_template")
    @patch("forms.SignupForm")
    def test_index_should_render_template_context(self, form, render):
        m = Mock()
        form.return_value = m
        render.return_value = ""
        reload(app)
        self.api.get("/")
        render.assert_called_with("index.html",
                                  facebook_app_id=app.FACEBOOK_APP_ID,
                                  github_client_id=app.GITHUB_CLIENT_ID,
                                  form=m)

    @patch("app.save_user")
    def test_signup(self, save):
        d = {"first_name": "Francisco", "last_name": "Souza",
             "email": "fss@corp.globo.com"}
        save.return_value = "user saved"
        app.SIGN_KEY = "key"
        resp = self.api.post("/signup", data=d)
        self.assertEqual(200, resp.status_code)
        self.assertEqual("user saved", resp.data)
        save.assert_called_with("Francisco", "Souza",
                                "fss@corp.globo.com")

    @patch("flask.render_template")
    @patch("forms.SignupForm")
    def test_signup_invalid_data(self, form, render):
        m = Mock()
        m.validate.return_value = False
        form.return_value = m
        render.return_value = "validation failed"
        d = {"first_name": "", "last_name": "", "email": "fss@corp.globo.com"}
        reload(app)
        resp = self.api.post("/signup", data=d)
        self.assertEqual(200, resp.status_code)
        self.assertEqual("validation failed", resp.data)
        form.assert_called_with(werkzeug.ImmutableMultiDict(d))
        render.assert_called_with("index.html",
                                  facebook_app_id=app.FACEBOOK_APP_ID,
                                  github_client_id=app.GITHUB_CLIENT_ID,
                                  form=m)


class FacebookLoginTestCase(ClientTest, unittest.TestCase):

    def _mock_requests(self, mock, data):
        m = Mock()
        m.json.return_value = data
        mock.return_value = m

    @patch("requests.get")
    @patch("app.save_user")
    def test_should_receive_facebook_data_and_store_on_database(self, save_user, mock):
        data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "first@last.com"
        }
        self._mock_requests(mock, data)
        save_user.return_value = ""
        resp = self.api.get(
            "/register/facebook?access_token=123awesometoken456"
        )
        self.assertEqual(200, resp.status_code)
        mock.get.assert_called_once()
        save_user.assert_called_with(data["first_name"],
                                     data["last_name"],
                                     data["email"])

    def test_return_400_and_not_save_user_when_validation_fails(self):
        resp = self.api.get("/register/facebook?access_token=")
        self.assertEqual(400, resp.status_code)


class GithubLoginTestCase(DatabaseTest, ClientTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ClientTest.setUpClass()
        DatabaseTest.setUpClass()
        app.SIGN_KEY = "key"

    @classmethod
    def tearDownClass(cls):
        app.SIGN_KEY = None

    def tearDown(self):
        self.db.users.remove()

    def _mock_requests(self, mock_post, mock_get, data_get, data_post):
        m = Mock()
        m.json.return_value = data_post
        mock_post.return_value = m
        m2 = Mock()
        m2.json.return_value = data_get
        mock_get.return_value = m2

    @patch("requests.post")
    @patch("requests.get")
    def test_should_request_be_success_and_redirect(self, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        resp = self.api.get("/register/github?code=coolcode")
        self.assertEqual(200, resp.status_code)

    def test_should_return_400_when_code_is_not_present(self):
        resp = self.api.get("/register/github")
        self.assertEqual(400, resp.status_code)

    @patch("requests.post")
    @patch("requests.get")
    def test_exchange_code_for_github_access_token(self, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        resp = self.api.get("/register/github?code=code21")
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, mock.call_count)
        self.assertEqual(1, mock_get.call_count)

    @patch("requests.post")
    @patch("requests.get")
    def test_should_store_user_in_database(self, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        resp = self.api.get("/register/github?code=code21")
        self.assertEqual(200, resp.status_code)
        u = self.db.users.find_one({"first_name": "Foo", "last_name": "Bar"})
        self.assertIsNotNone(u)
        self.assertEqual(u["email"], "test@test.com")

    @patch("requests.post")
    @patch("requests.get")
    @patch("flask.render_template")
    def test_confirmation_with_email_and_sign(self, render, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        render.return_value = ""
        reload(app)
        app.SIGN_KEY = "key"
        resp = self.api.get("/register/github?code=code21")
        self.assertEqual(200, resp.status_code)
        render.assert_called_with("confirmation.html",
                                  email="test@test.com",
                                  signature=app.sign("test@test.com"))


class GplusLoginTestCase(ClientTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        mongo_uri_port = app.MONGO_URI.split(":")
        host = mongo_uri_port[0]
        port = int(mongo_uri_port[1])
        cls.conn = Connection(host, port)
        cls.db = cls.conn[app.MONGO_DATABASE_NAME]
        ClientTest.setUpClass()
        app.SIGN_KEY = "key"

    @classmethod
    def tearDownClass(cls):
        app.SIGN_KEY = None

    def tearDown(self):
        self.db.users.remove()

    def clean_api_client(self):
        app.GOOGLE_USER_IP = None
        app.GOOGLE_API_KEY = None

    def test_should_return_bad_request_when_token_is_missing(self):
        resp = self.api.get("/register/gplus")
        self.assertEqual(400, resp.status_code)
        self.assertEqual(u"Token is required.", resp.data)

    def test_should_return_bad_request_when_token_type_is_missing(self):
        resp = self.api.get("/register/gplus?token=mytoken")
        self.assertEqual(400, resp.status_code)
        self.assertEqual(u"Token is required.", resp.data)

    @patch("requests.get")
    def test_should_send_request_to_google_plus(self, mock):
        app.GOOGLE_USER_IP = "127.0.0.1"
        app.GOOGLE_API_KEY = "key"
        app.SIGN_KEY = "key"
        self.addCleanup(self.clean_api_client)
        m = Mock()
        m.json.return_value = {
            "id": "1234",
            "email": "secret@company.com",
            "verified_email": True,
            "given_name": "Francisco",
            "family_name": "Souza",
            "name": "Francisco Souza",
            "gender": "male",
        }
        mock.return_value = m
        resp = self.api.get("/register/gplus?token=mytoken&token_type=Bearer")
        self.assertEqual(200, resp.status_code)
        url = "{0}/userinfo?key={1}&userIp={2}".format(
            app.GOOGLE_OAUTH_ENDPOINT,
            app.GOOGLE_API_KEY,
            app.GOOGLE_USER_IP
        )
        headers = {"Authorization": "Bearer mytoken"}
        mock.assert_called_with(url, headers=headers)
        u = self.db.users.find_one({
            "email": "secret@company.com",
            "first_name": "Francisco",
            "last_name": "Souza"
        })
        self.assertIsNotNone(u)

    @patch("requests.get")
    @patch("flask.render_template")
    def test_confirmation_template_with_email_in_context(self, render, get):
        app.GOOGLE_USER_IP = "127.0.0.1"
        app.GOOGLE_API_KEY = "key"
        self.addCleanup(self.clean_api_client)
        m = Mock()
        m.json.return_value = {
            "id": "1234",
            "email": "secret@company.com",
            "verified_email": True,
            "given_name": "Francisco",
            "family_name": "Souza",
            "name": "Francisco Souza",
            "gender": "male",
        }
        get.return_value = m
        render.return_value = ""
        reload(app)
        app.SIGN_KEY = "key"
        resp = self.api.get("/register/gplus?token=mytoken&token_type=Bearer")
        self.assertEqual(200, resp.status_code)
        render.assert_called_with("confirmation.html",
                                  email="secret@company.com",
                                  signature=app.sign("secret@company.com"))

    @patch("requests.get")
    @patch("flask.render_template")
    def test_form_when_user_is_already_registered(self, render, get):
        app.GOOGLE_USER_IP = "127.0.0.1"
        app.GOOGLE_API_KEY = "key"
        self.addCleanup(self.clean_api_client)
        m = Mock()
        m.json.return_value = {
            "id": "1234",
            "email": "secret@company.com",
            "verified_email": True,
            "given_name": "Francisco",
            "family_name": "Souza",
            "name": "Francisco Souza",
            "gender": "male",
        }
        get.return_value = m
        render.return_value = ""
        self.db.users.insert({
            "email": "secret@company.com",
            "first_name": "Francisco",
            "last_name": "Souza"
        })
        reload(app)
        resp = self.api.get("/register/gplus?token=mytoken&token_type=Bearer")
        self.assertEqual(200, resp.status_code)
        render.assert_called_with("confirmation.html", registered=True)


class HelperTestCase(DatabaseTest, unittest.TestCase):

    def test_has_token_should_check_for_access_token(self):
        is_valid = app.has_token({"access_token": "123token"})
        self.assertTrue(is_valid)

    def test_has_token_should_return_false_when_value_is_empty(self):
        is_valid = app.has_token({"access_token": ""})
        self.assertFalse(is_valid)

    def test_parse_github_name_splits_correctly_with_both_names(self):
        first, last = app.parse_github_name({"name": "First Last"})
        self.assertEqual(first, "First")
        self.assertEqual(last, "Last")

    def test_parse_github_name_splits_correctly_with_more_than_two_names(self):
        first, last = app.parse_github_name(
            {"name": "First Lots Of Other Names Last"}
        )
        self.assertEqual(first, "First")
        self.assertEqual(last, "Last")

    def test_parse_github_name_splits_correctly_with_only_one_name(self):
        first, last = app.parse_github_name({"name": "First"})
        self.assertEqual(first, "First")
        self.assertEqual(last, "")

    def test_sign(self):
        app.SIGN_KEY = "123456"
        email = "fss@corp.globo.com"
        expected = hashlib.sha1(email + app.SIGN_KEY).hexdigest()
        self.assertEqual(expected, app.sign(email))

    @patch("flask.render_template")
    def test_save_user(self, render):
        render.return_value = "template rendered"
        reload(app)
        app.SIGN_KEY = "123456"
        with app.app.test_request_context("/"):
            app.before_request()
            content, status = app.save_user("Francisco", "Souza",
                                            "fss@corp.globo.com")
            app.teardown_request(None)
        self.assertEqual("template rendered", content)
        self.assertEqual(200, status)
        render.assert_called_with("confirmation.html",
                                  email="fss@corp.globo.com",
                                  signature=app.sign("fss@corp.globo.com"))
        u = self.db.users.find_one({
            "email": "fss@corp.globo.com",
            "first_name": "Francisco",
            "last_name": "Souza",
        })
        self.assertIsNotNone(u)

    @patch("flask.render_template")
    def test_save_user_duplicate(self, render):
        self.db.users.insert({
            "email": "fss@corp.globo.com",
            "first_name": "Chico",
            "last_name": "Souza",
        })
        render.return_value = "another template rendered"
        reload(app)
        with app.app.test_request_context("/"):
            app.before_request()
            content, status = app.save_user("Francisco", "Souza",
                                            "fss@corp.globo.com")
            app.teardown_request(None)
        self.assertEqual("another template rendered", content)
        self.assertEqual(200, status)
        render.assert_called_with("confirmation.html",
                                  registered=True)


class SurveyTestCase(DatabaseTest, ClientTest, unittest.TestCase):

    def test_save(self):
        data = {
            "email": "some@email.com",
            "work": "work",
            "country": "china",
            "organization": "organization",
            "why": "why",
        }
        resp = self.api.post("/survey", data=data)
        self.assertEqual(201, resp.status_code)
        s = self.db.survey.find_one({"email": "some@email.com"})
        self.assertIsNotNone(s)
