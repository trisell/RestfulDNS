from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms.validators import Regexp

class RegisterForm(Form):
	hostname = TextField('Hostname',validators=[DataRequired()])
	ipaddress = TextField('IP Address', validators=[Regexp(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", message='Please enter a valid IP address')])

class DeleteForm(Form):
	hostname = TextField('Hostname',validators=[DataRequired()])
	ipaddress = TextField('IP Address', validators=[Regexp(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", message='Please enter a valid IP address')])
