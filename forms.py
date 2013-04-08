import wtforms
from flask.ext import wtf
from wtforms import validators


class SignupForm(wtf.Form):
    first_name = wtforms.TextField(u"First name",
                                   validators=[validators.DataRequired()])
    last_name = wtforms.TextField(u"Last name",
                                  validators=[validators.DataRequired()])
    email = wtforms.TextField(u"Email", validators=[validators.DataRequired(),
                                                    validators.Email()])


class SurveyForm(wtf.Form):
    email = wtforms.HiddenField(u"email",
                                validators=[validators.DataRequired(),
                                            validators.Email()])
    signature = wtforms.HiddenField(u"signature",
                                    validators=[validators.DataRequired()])
