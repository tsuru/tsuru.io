import unittest

import wtforms
from flask.ext import wtf
from wtforms import validators

import forms


class SurveyFormTestCase(unittest.TestCase):

    def test_should_be_a_wtform(self):
        assert issubclass(forms.SurveyForm, wtf.Form)


class SignupFormTestCase(unittest.TestCase):

    def test_should_be_a_wtform(self):
        assert issubclass(forms.SignupForm, wtf.Form)

    def test_first_name_should_be_text_field(self):
        field = forms.SignupForm.first_name
        self.assertEqual(wtforms.TextField, field.field_class)

    def test_first_name_label(self):
        field = forms.SignupForm.first_name
        self.assertEqual(u"First name", field.args[0])

    def test_first_name_should_be_mandatory(self):
        field = forms.SignupForm.first_name
        self.assertIsInstance(field.kwargs["validators"][0],
                              validators.DataRequired)

    def test_last_name_should_be_text_field(self):
        field = forms.SignupForm.last_name
        self.assertEqual(wtforms.TextField, field.field_class)

    def test_last_name_label(self):
        field = forms.SignupForm.last_name
        self.assertEqual(u"Last name", field.args[0])

    def test_last_name_should_be_mandatory(self):
        field = forms.SignupForm.last_name
        self.assertIsInstance(field.kwargs["validators"][0],
                              validators.DataRequired)

    def test_email_should_be_text_field(self):
        field = forms.SignupForm.email
        self.assertEqual(wtforms.TextField, field.field_class)

    def test_email_label(self):
        field = forms.SignupForm.email
        self.assertEqual(u"Email", field.args[0])

    def test_email_should_be_mandatory(self):
        field = forms.SignupForm.email
        self.assertIsInstance(field.kwargs["validators"][0],
                              validators.DataRequired)

    def test_email_should_require_valid_email(self):
        field = forms.SignupForm.email
        self.assertIsInstance(field.kwargs["validators"][1],
                              validators.Email)
