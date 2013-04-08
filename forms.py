import wtforms
from flask.ext import wtf
from wtforms import validators


class SignupForm(wtf.Form):
    first_name = wtforms.TextField(u"First name",
                                   validators=[validators.Required()])
    last_name = wtforms.TextField(u"Last name",
                                  validators=[validators.Required()])
    email = wtforms.TextField(u"Email", validators=[validators.Required(),
                                                    validators.Email()])
