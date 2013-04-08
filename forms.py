# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import wtforms
from flask.ext import wtf
from wtforms import validators
from countries import country_choices
from flaskext.babel import gettext


class SignupForm(wtf.Form):
    first_name = wtforms.TextField(gettext(u"First name"),
                                   validators=[validators.DataRequired()])
    last_name = wtforms.TextField(gettext(u"Last name"),
                                  validators=[validators.DataRequired()])
    email = wtforms.TextField(
        gettext(u"Email"),
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
        ("developer", gettext("Developer")),
        ("manager", gettext("Project Manager")),
        ("researcher", gettext("Researcher")),
        ("student", gettext("Student")),
        ("teacher", gettext("Teacher")),
        ("ops", gettext("Ops")),
        ("", gettext("Other"))
    ]
    work = wtforms.SelectField(gettext(u"What do you do for a living?"),
                               choices=choices)
    country = wtforms.SelectField(gettext(u"Where do you live?"),
                                  choices=country_choices)
    organization = wtforms.TextField(gettext(u"What is your company name?"))
    choices = [("build", gettext("Build my own PaaS")),
               ("compare", gettext("Compare to other PaaS")),
               ("deploy", gettext("Deploy my apps")),
               ("curious", gettext("I'm just curious")),
               ("", gettext("Other"))]
    why = wtforms.SelectField(gettext(u"Why do you want to try tsuru?"),
                              choices=choices)
