from flask import Flask, Flask, jsonify, redirect, url_for, request, render_template, abort, Response
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
from psw import hash_password, verify_password
from createToken import generate_auth_token, verify_auth_token

from wtforms import Form, StringField, PasswordField
from wtforms.validators import InputRequired, DataRequired

from flask import Flask, Response
from flask_login import LoginManager, UserMixin, login_required

# WHAT LIBRARIES DO I INSTALL?


app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

login_manager = LoginManager()
login_manager.init_app(app)

client = MongoClient('db', 27017)
db = client.tododb # gets database
db2 = client.users # inserts another db doc called users

#db2.users.delete_many({})

# Register User through register form and save in db
# Log user in (check pass hash) - returns a token?

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

class RegistrationForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

@app.route('/register', methods=['GET','POST'])
def register(request):
	form = RegistrationForm(request.POST)
	'''
	if request.method == 'POST' and form.validate():
		in_db = db2.users.find_one( { 'username': form.username.data })
		if in_db != None: # if username is already taken
			app.logger.debug("USER ALREADY EXISTS")
			return render_template("400.html"), 400
		
		hashed_pass = hash_password(form.password.data)
		
		# inserts user into data base
		db_user = { 'username': form.username.data, 'password': hashed_pass }
		db2.users.insert_one(db_user)	
		
		# creates a user object with credentials
		user = User(form.username.data,hashed_pass)
		user.save()
		
		return redirect('/login'),201
	
	return render_response('register.html',form=form)
	'''
	return render_template(register.html,form=form)
		

class User(UserMixin):
	def __init__(self,username,password):
		self.id = username
		self.password = password
		
	@classmethod
	def get(cls,token): #WHAT IS THIS RETURNING?
		user = db2.users.find_one({'username': username})
		return cls.user['_id']

@login_manager.request_loader
def load_user(request):
	pass

@login_manager.request_loader
def load_user_from_request(request):
	token = request.args.get('token')
	if token != None:
		verified = verify_auth_token(token,app.config['SECRET_KEY'])

@app.route('/login', methods=['GET','POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():		
		# find whether the user exists in db
		user = db2.users.find_one( { 'username': form.username.data })
		app.logger.debug("User Exists! " + str(user))
		
		# verify users password
		hashed_pass = user['password']
		passVerify = verify_password(form.password.data,hashed_pass)
		app.logger.debug("Password Verified? " + str(passVerify))
		
		if passVerify == False:
			return render_template("401.html"), 401
		


			
		