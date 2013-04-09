import hashlib
import os
import unittest

import werkzeug
from mock import patch, Mock
from pymongo import Connection

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

    @patch("flask.render_template")
    def test_about(self, render):
        render.return_value = "about rendered"
        reload(app)
        resp = self.api.get("/about")
        self.assertEqual("about rendered", resp.data)
        render.assert_called_with("about.html")

    @patch("flask.render_template")
    def test_community(self, render):
        render.return_value = "community rendered"
        reload(app)
        resp = self.api.get("/community")
        self.assertEqual("community rendered", resp.data)
        render.assert_called_with("community.html")

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
        self.api.get("/try")
        render.assert_called_with("try.html",
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
        render.assert_called_with("try.html",
                                  facebook_app_id=app.FACEBOOK_APP_ID,
                                  github_client_id=app.GITHUB_CLIENT_ID,
                                  form=m)

    def test_bucket_support(self):
        os.environ["TSURU_S3_BUCKET"] = "mybucket"
        self.addCleanup(reload, app)
        reload(app)
        self.assertEqual("mybucket", app.app.config["S3_BUCKET_NAME"])
        del os.environ["TSURU_S3_BUCKET"]


class FacebookLoginTestCase(DatabaseTest, ClientTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        DatabaseTest.setUpClass()
        ClientTest.setUpClass()

    def _mock_requests(self, mock, data):
        m = Mock()
        m.json.return_value = data
        mock.return_value = m

    @patch("requests.get")
    @patch("app.save_user")
    def test_should_store_facebook_data_on_database(self, save_user, mock):
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
        save_user.assert_called_with(data["first_name"],
                                     data["last_name"],
                                     data["email"])

    @patch("requests.get")
    @patch("flask.render_template")
    def test_confirmation_template_with_email_and_signature(self, render, get):
        data = {
            "first_name": "First",
            "last_name": "Last",
            "email": "first@last.com"
        }
        self._mock_requests(get, data)
        render.return_value = ""
        reload(app)
        app.SIGN_KEY = "key"
        self.addCleanup(lambda: self.db.users.remove())
        with patch("app.get_survey_form"):
            resp = self.api.get(
                "/register/facebook?access_token=123awesometoken456"
            )
            self.assertEqual(200, resp.status_code)
            render.assert_called_with("confirmation.html",
                                      form=app.get_survey_form(data["email"]))

    def test_return_400_and_not_save_user_when_validation_fails(self):
        resp = self.api.get("/register/facebook?access_token=")
        self.assertEqual(400, resp.status_code)


class GithubLoginTestCase(ClientTest, unittest.TestCase):

    def _mock_requests(self, mock_post, mock_get, data_get, data_post):
        m = Mock()
        m.json.return_value = data_post
        mock_post.return_value = m
        m2 = Mock()
        m2.json.return_value = data_get
        mock_get.return_value = m2

    @patch("requests.post")
    @patch("requests.get")
    @patch("app.save_user")
    def test_should_return_200_with_code(self, save_user, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        save_user.return_value = ""
        resp = self.api.get("/register/github?code=coolcode")
        self.assertEqual(200, resp.status_code)

    def test_should_return_400_when_code_is_not_present(self):
        resp = self.api.get("/register/github")
        self.assertEqual(400, resp.status_code)

    @patch("requests.post")
    @patch("requests.get")
    @patch("app.save_user")
    def test_get_access_token_from_github(self, save_user, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        save_user.return_value = ""
        resp = self.api.get("/register/github?code=code21")
        self.assertEqual(200, resp.status_code)
        self.assertEqual(1, mock.call_count)
        self.assertEqual(1, mock_get.call_count)

    @patch("requests.post")
    @patch("requests.get")
    @patch("app.save_user")
    def test_should_store_user_in_database(self, save_user, mock_get, mock):
        self._mock_requests(mock, mock_get,
                            {"email": "test@test.com", "name": "Foo Bar"},
                            {"access_token": "testtoken"})
        save_user.return_value = ""
        resp = self.api.get("/register/github?code=code21")
        self.assertEqual(200, resp.status_code)
        save_user.assert_called_with("Foo", "Bar", "test@test.com")

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
        with patch("app.get_survey_form"):
            resp = self.api.get("/register/github?code=code21")
            self.assertEqual(200, resp.status_code)
            render.assert_called_with("confirmation.html",
                                      form=app.get_survey_form("test@test.com")
                                      )


class GplusLoginTestCase(ClientTest, unittest.TestCase):

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
    @patch("app.save_user")
    def test_should_send_request_to_google_plus(self, save_user, mock):
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
        save_user.return_value = ""
        resp = self.api.get("/register/gplus?token=mytoken&token_type=Bearer")
        self.assertEqual(200, resp.status_code)
        url = "{0}/userinfo?key={1}&userIp={2}".format(
            app.GOOGLE_OAUTH_ENDPOINT,
            app.GOOGLE_API_KEY,
            app.GOOGLE_USER_IP
        )
        headers = {"Authorization": "Bearer mytoken"}
        mock.assert_called_with(url, headers=headers)
        save_user.assert_called_with("Francisco", "Souza",
                                     "secret@company.com",
                                     redirect_to="/")

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
        with patch("app.get_survey_form"):
            resp = self.api.get(
                "/register/gplus?token=mytoken&token_type=Bearer"
            )
            self.assertEqual(200, resp.status_code)
            render.assert_called_with("confirmation.html",
                                      form=app.get_survey_form(
                                      "secret@company.com"
                                      ))

    @patch("requests.get")
    def test_form_when_user_is_already_registered(self, get):
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
        resp = self.api.get("/register/gplus?token=mytoken&token_type=Bearer")
        self.assertEqual(302, resp.status_code)
        self.assertEqual("http://localhost/", resp.headers["Location"])


class HelperTestCase(DatabaseTest, unittest.TestCase):

    def test_has_token_without_access_token(self):
        is_valid = app.has_token({})
        self.assertFalse(is_valid)

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
        with patch("app.get_survey_form"):
            with app.app.test_request_context("/"):
                app.before_request()
                content, status = app.save_user("Francisco", "Souza",
                                                "fss@corp.globo.com")
                app.teardown_request(None)
            self.assertEqual("template rendered", content)
            self.assertEqual(200, status)
            render.assert_called_with("confirmation.html",
                                      form=app.get_survey_form(
                                      "fss@corp.globo.com"))
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

    @patch("flask.request")
    def test_get_locale(self, request):
        request.accept_languages.best_match.return_value = "en"
        request.cookies = {}
        reload(app)
        result = app.get_locale()
        self.assertEqual("en", result)
        request.accept_languages.best_match.assert_called_with(["pt", "en"])

    @patch("flask.request")
    def test_get_locale_from_cookie(self, request):
        request.cookies = {"language": "pt"}
        reload(app)
        result = app.get_locale()
        self.assertEqual("pt", result)

    @patch("flask.render_template")
    def test_save_user_should_pass_form_to_template(self, mock):
        reload(app)
        app.SIGN_KEY = "test_key"
        with patch("app.get_survey_form"):
            with app.app.test_request_context("/"):
                app.before_request()
                app.save_user("First", "Last", "first@last.com")
                app.teardown_request(None)
            mock.assert_called_with("confirmation.html",
                                    form=app.get_survey_form("first@last.com"))
        app.SIGN_KEY = None

    @patch("forms.SurveyForm")
    def test_get_survey_form_should_return_form(self, mock):
        app.SIGN_KEY = "test_key"
        app.get_survey_form("test@test.com")
        mock.assert_called_once()
        app.SIGN_KEY = None

    @patch("forms.SurveyForm")
    def test_get_survey_form_should_initializa_email_field(self, mock):
        app.SIGN_KEY = "test_key"
        email = "test@test.com"
        form = app.get_survey_form(email)
        self.assertEqual(email, form.email.data)
        app.SIGN_KEY = None

    @patch("forms.SurveyForm")
    def test_get_survey_form_should_initialize_signature_field(self, mock):
        app.SIGN_KEY = "test_key"
        email = "test@test.com"
        form = app.get_survey_form(email)
        self.assertEqual(app.sign(email), form.signature.data)
        app.SIGN_KEY = None

    def test_get_survey_form_with_request_form(self):
        app.SIGN_KEY = "test_key"
        email = "test@test.com"
        d = {"work": "dba"}
        with app.app.test_request_context("/"):
            form = app.get_survey_form(email, werkzeug.ImmutableMultiDict(d))
            self.assertEqual("dba", form.work.data)
        app.SIGN_KEY = None


class SurveyTestCase(DatabaseTest, ClientTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ClientTest.setUpClass()
        DatabaseTest.setUpClass()

    @classmethod
    def tearDownClass(cls):
        app.SIGN_KEY = None

    def test_save(self):
        reload(app)  # this unmocks render_template
        app.SIGN_KEY = "sig_key"
        data = {
            "email": "test@test.me",
            "signature": app.sign("test@test.me"),
            "work": "student",
            "country": "Brazil",
            "organization": "organization",
            "why": "deploy",
        }
        resp = self.api.post("/survey", data=data)
        self.assertEqual(201, resp.status_code)
        s = self.db.survey.find_one({"email": data["email"]})
        self.assertIsNotNone(s)

    def test_should_return_400_when_data_is_invalid(self):
        data = {
            "email": "invalid email",
            "signature": app.sign("some@email.com"),
            "work": "ops",
            "country": "Brazil",
            "organization": "organization",
            "why": "compare",
        }
        app.SIGN_KEY = "sig_key"
        resp = self.api.post("/survey", data=data)
        self.assertEqual(400, resp.status_code)

    def test_should_should_return_400_when_signatures_doesnt_match(self):
        app.SIGN_KEY = "sig_key"
        data = {
            "email": "email@test.com",
            "signature": app.sign("some@email.com"),
            "work": "ops",
            "country": "Brazil",
            "organization": "organization",
            "why": "compare",
        }
        resp = self.api.post("/survey", data=data)
        self.assertEqual(400, resp.status_code)
        expected = ("Signatures don't match. "
                    "You're probably doing something nasty.")
        self.assertEqual(expected, resp.data)

    @patch("flask.render_template")
    def test_should_render_confirmation_template_registered(self, render):
        render.return_value = ""
        reload(app)
        app.SIGN_KEY = "sig_key"
        data = {
            "email": "some@email.com",
            "signature": app.sign("some@email.com"),
            "work": "ops",
            "country": "Brazil",
            "organization": "organization",
            "why": "compare",
        }
        resp = self.api.post("/survey", data=data)
        self.assertEqual(201, resp.status_code)
        render.assert_called_once_with("confirmation.html", registered=True)
