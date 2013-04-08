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
    choices = [("cio", "CIO"), ("cto", "CTO"), ("dba", "DBA"),
               ("developer", "Developer"), ("manager", "Project Manager"),
               ("researcher", "Researcher"), ("student", "Student"),
               ("teacher", "Tearcher"), ("ops", "Ops"), ("", "Other")]
    work = wtforms.SelectField(u"What do you do for a living?",
                               choices=choices,
                               validators=[validators.DataRequired()])
    country = wtforms.SelectField(u"Where do you live?",
                                  choices=country_choices,
                                  validators=[validators.DataRequired()])
    organization = wtforms.TextField(u"What is your company name?",
                                     validators=[validators.DataRequired()])
    choices = [("build", "Build my own PaaS"),
               ("compare", "Compare to other PaaS"),
               ("deploy", "Deploy my apps"),
               ("curious", "I'm just curious"),
               ("", "Other")]
    why = wtforms.SelectField(u"Why do you want to try tsuru?",
                              choices=choices,
                              validators=[validators.DataRequired()])
