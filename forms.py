# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import wtforms
from flask.ext import wtf
from wtforms import validators
from countries import country_choices
from flaskext.babel import lazy_gettext


class SignupForm(wtf.Form):
    first_name = wtforms.TextField(lazy_gettext(u"First name"),
                                   validators=[validators.DataRequired()])
    last_name = wtforms.TextField(lazy_gettext(u"Last name"),
                                  validators=[validators.DataRequired()])
    email = wtforms.TextField(
        lazy_gettext(u"Email"),
        validators=[validators.DataRequired(), validators.Email()]
    )


class SurveyForm(wtf.Form):
    email = wtforms.HiddenField(u"email",
                                validators=[validators.DataRequired(),
                                            validators.Email()])
    signature = wtforms.HiddenField(u"signature",
                                    validators=[validators.DataRequired()])
    choices = [
        ("cio", "CIO"),
        ("cto", "CTO"),
        ("dba", "DBA"),
        ("developer", lazy_gettext("Developer")),
        ("manager", lazy_gettext("Project Manager")),
        ("researcher", lazy_gettext("Researcher")),
        ("student", lazy_gettext("Student")),
        ("teacher", lazy_gettext("Teacher")),
        ("ops", lazy_gettext("Ops")),
        ("", lazy_gettext("Other"))
    ]
    work = wtforms.SelectField(lazy_gettext(u"What do you do for a living?"),
                               choices=choices)
    country = wtforms.SelectField(lazy_gettext(u"Where do you live?"),
                                  choices=country_choices)
    organization = wtforms.TextField(lazy_gettext(u"What is your company name?"))
    choices = [("build", lazy_gettext("Build my own PaaS")),
               ("compare", lazy_gettext("Compare to other PaaS")),
               ("deploy", lazy_gettext("Deploy my apps")),
               ("curious", lazy_gettext("I'm just curious")),
               ("", lazy_gettext("Other"))]
    why = wtforms.SelectField(lazy_gettext(u"Why do you want to try tsuru?"),
                              choices=choices)
