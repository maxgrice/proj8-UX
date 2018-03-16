from flask.ext.wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class RegistrationForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])
	