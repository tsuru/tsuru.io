# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

import wtforms
from flask.ext import wtf
from wtforms import validators

import forms


class SurveyFormTestCase(unittest.TestCase):

    def test_should_be_a_wtform(self):
        assert issubclass(forms.SurveyForm, wtf.Form)

    def test_email_should_be_hidden_field(self):
        field = forms.SurveyForm.email
        self.assertEqual(wtforms.HiddenField, field.field_class)

    def test_signature_should_be_hidden_field(self):
        field = forms.SurveyForm.signature
        self.assertEqual(wtforms.HiddenField, field.field_class)

    def test_work_field_should_be_select_feld(self):
        field = forms.SurveyForm.work
        self.assertEqual(wtforms.SelectField, field.field_class)

    def test_work_field_should_have_choices(self):
        expected = [("", "Please select"), ("cio", "CIO"), ("cto", "CTO"),
                    ("dba", "DBA"), ("developer", "Developer"),
                    ("manager", "Project Manager"),
                    ("researcher", "Researcher"), ("student", "Student"),
                    ("teacher", "Teacher"), ("ops", "Ops"), ("", "Other")]
        choices = forms.SurveyForm.work.kwargs["choices"]
        self.assertListEqual(expected, choices)

    def test_why_field_should_have_choices(self):
        expected = [("", "Please select"),
                    ("build", "Build my own PaaS"),
                    ("compare", "Compare to other PaaS"),
                    ("deploy", "Deploy my apps"),
                    ("curious", "I'm just curious"),
                    ("", "Other")]
        choices = forms.SurveyForm.why.kwargs["choices"]
        self.assertEqual(expected, choices)


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

    def test_identity_should_be_text_field(self):
        field = forms.SignupForm.identity
        self.assertEqual(wtforms.TextField, field.field_class)

    def test_identity_label(self):
        field = forms.SignupForm.identity
        self.assertEqual(u"Identity", field.args[0])

    def test_identity_should_be_mandatory(self):
        field = forms.SignupForm.identity
        self.assertIsInstance(field.kwargs["validators"][0],
                              validators.DataRequired)

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
