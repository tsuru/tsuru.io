# Copyright 2013 Globo.com. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import wtforms
from flask.ext import wtf
from wtforms import validators
from flaskext.babel import lazy_gettext as _


class SignupForm(wtf.Form):
    first_name = wtforms.TextField(_("First name"),
                                   validators=[validators.DataRequired()])
    last_name = wtforms.TextField(_("Last name"),
                                  validators=[validators.DataRequired()])
    email = wtforms.TextField(
        _(u"Email"),
        validators=[validators.DataRequired(), validators.Email()]
    )

    identity = wtforms.TextField(
        _(u"Identity"),
        validators=[validators.DataRequired()]
    )


class SurveyForm(wtf.Form):
    email = wtforms.HiddenField(u"email",
                                validators=[validators.DataRequired(),
                                            validators.Email()])
    signature = wtforms.HiddenField(u"signature",
                                    validators=[validators.DataRequired()])
    choices = [
        ("", _("Please select")),
        ("cio", "CIO"),
        ("cto", "CTO"),
        ("dba", "DBA"),
        ("developer", _("Developer")),
        ("manager", _("Project Manager")),
        ("researcher", _("Researcher")),
        ("student", _("Student")),
        ("teacher", _("Teacher")),
        ("ops", _("Ops")),
        ("", _("Other"))
    ]
    work = wtforms.SelectField(_("What do you do for a living?"),
                               choices=choices)
    country = wtforms.SelectField(_("Where do you live?"), coerce=str)
    organization = wtforms.TextField(_("What is your company name?"))
    choices = [
        ("", _("Please select")),
        ("build", _("Build my own PaaS")),
        ("compare", _("Compare to other PaaS")),
        ("deploy", _("Deploy my apps")),
        ("curious", _("I'm just curious")),
        ("", _("Other"))
    ]
    why = wtforms.SelectField(_(u"Why do you want to try tsuru?"),
                              choices=choices)
