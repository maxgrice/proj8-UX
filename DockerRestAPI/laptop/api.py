# Laptop Service
from flask import Flask, Flask, jsonify, redirect, url_for, request, render_template, abort, flash
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
from psw import hash_password, verify_password
#from createToken import generate_auth_token, verify_auth_token

from flask.json import JSONEncoder

from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length

from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

from itsdangerous import (TimedJSONWebSignatureSerializer \
                                  as Serializer, BadSignature, \
                                  SignatureExpired)
import time

import random

# Instantiate the app
app = Flask(__name__)
api = Api(app)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

# ACCESS DATABASE
client = MongoClient('db', 27017)
db = client.tododb # gets database
db2 = client.users # inserts another db doc called users

db2.users.delete_many({})

class User():
	def __init__(self,username):
		self.username = username
	def is_authenticated(self):
		return True	
	def is_active(self):
		return True	
	def is_anonymous(self):
		return False	
	def get_id(self):
		return self.username
		
	@staticmethod
	def validate_login(password,hashed_pass):
		return verify_password(password,hashed_pass)
	
	def generate_auth_token(self,secret,user_id,expiration):
		s = Serializer(secret, expires_in=expiration)
		# pass index of user
		return s.dumps(user_id) # hashes with given user id
	
	@staticmethod
	def verify_auth_token(token,secret):
		s = Serializer(secret) # WHAT IS SERIALIZER?
		try:
			data = s.loads(token) # Decodes the hash
		except SignatureExpired:
			return False    # valid token, but expired
		except BadSignature:
			return False    # invalid token
		return True

class RegistrationForm(Form):
	username = StringField('username',[DataRequired(message='Please Enter a Username!')])
	password = PasswordField('password',[DataRequired(message='Please Enter a Password!')])

class LoginForm(Form):
	username = StringField('username', validators=[DataRequired()])
	password = PasswordField('password', validators=[DataRequired()])

@login_manager.user_loader
def load_user(username):
	user = db2.users.find_one({'username': username})
	if user == None:
		return None
	return User(user['_id'])

@app.route('/api/register', methods=['GET','POST'])
def register(): # takes you to the sign up page
	form = RegistrationForm(request.form)
	
	_items = db2.users.find()
	items = [item for item in _items]
	app.logger.debug(items)
	app.logger.debug("On Registeration Page")

	username = form.username.data
	password = form.password.data
	
	app.logger.debug("UserName: " + str(form.username.data))
	app.logger.debug("Password: " + str(form.password.data))
	
	if request.method == 'POST' and form.validate():
		app.logger.debug("Now Validating Credentials...")
		user = db2.users.find_one({'username': form.username.data})

		if user != None: # User is already in the data base
			app.logger.debug("USER ALREADY EXISTS!")
			flash("user already exists!")
			return render_template("401.html"), 401
			
		hashed_pass = hash_password(password)
		new_user = { 'username': username, 'password': hashed_pass }
		db2.users.insert_one(new_user)
		
		new_user = db2.users.find_one({'username': username})
		result = { 'username': new_user['username'], 'password': new_user['password'], '_id': str(new_user['_id']) } 
		
		return jsonify(result=result), 201

	flash("please enter a valid username and password")
	return render_template('register.html',form=form)

@app.route('/api/token', methods=['GET', 'POST'])
def login(): # takes you to the sign up page
	form = LoginForm(request.form)
	
	username = form.username.data
	password = form.password.data
	
	app.logger.debug("UserName: " + str(username))
	app.logger.debug("Password: " + str(password))
	
	if request.method == 'POST' and form.validate():
		app.logger.debug("Validating Credentials...")
		userDB = db2.users.find_one( { 'username': username } )
		if userDB!=None and User.validate_login(form.password.data,userDB['password']):
			user = User(str(userDB['_id']))
			login_user(user,remember=True)
			flash("Your login credentials are valid", category='success')

			user_id = userDB['_id']
			app.logger.debug("Id type " + str(type(user_id)))
			id = { 'id' : str(user_id) }
			app.logger.debug(id)
			token = user.generate_auth_token(app.config['SECRET_KEY'],id,600)
			app.logger.debug("MADE TOKEN")
			token = token.decode('utf-8')
			app.logger.debug("Token Type " + str(type(token)))
			result = { 'token': token, 'duration': 30 }
			#result = EqtlByToken(token,30)
			app.logger.debug("RESULT TYPE " + str(type(result)))
			app.logger.debug(result)
			return jsonify(result=result), 201
			
		
		app.logger.debug("Your credentials were invalid, please try again")
		return render_template("401.html"), 401		
	
	return render_template('login.html',form=form)

@app.route('/logout')
def logout():
	rand_num = random.randint(1,100)
	app.config['SECRET_KEY'] = app.config['SECRET_KEY'] + str(rand_num)
	logout_user()
	return redirect(url_for('login'))

class all(Resource): # USE 5001 TO ACCESS!
	def get(self):
		app.logger.debug("CHECKING RESOURCE")
		token = request.args.get('token') 
		app.logger.debug("TOKEN " + str(token))

		if token == None: # makes sure a token was entered
			app.logger.debug("TOKEN NOT FOUND ")
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		app.logger.debug("VERIFIED IS " + str(verified))
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:	
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]

			app.logger.debug("DATA IS")
			app.logger.debug(li_data)
		
			dic = {}
			otimes = []
			ctimes = []
		
			for item in li_data:
				otimes.append(item['open_times'])
				ctimes.append(item['close_times'])
			
			app.logger.debug("OPEN IS")
			app.logger.debug(otimes)
			app.logger.debug("CLOSE IS")
			app.logger.debug(ctimes)
		
			dic['open_times'] = otimes
			dic['close_times'] = ctimes
			
			app.logger.debug("DICTIONARY")
			app.logger.debug(dic)
		
			return dic
		
api.add_resource(all, '/listAll')

class all_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]		
			dic = {}
			otimes = []
			ctimes = []		
			for item in li_data:
				otimes.append(item['open_times'])
				ctimes.append(item['close_times'])		
			dic['open_times'] = otimes
			dic['close_times'] = ctimes
			return dic

api.add_resource(all_json, '/listAll/json')

class all_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['open_times'] + ", "
				csv_string += item['close_times'] + ", "
			return csv_string

api.add_resource(all_csv, '/listAll/csv')

class open_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('open_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			app.logger.debug("MADE IT HERE")
			dic = {}
			otimes = []	
			for item in li_data:
				otimes.append(item['open_times'])		
			dic['open_times'] = otimes
			return dic

api.add_resource(open_json, '/listOpenOnly/json')

class open_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('open_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['open_times'] + ", "
			return csv_string

api.add_resource(open_csv, '/listOpenOnly/csv')

class close_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('close_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			dic = {}
			ctimes = []		
			for item in li_data:
				ctimes.append(item['close_times'])		
				dic['close_times'] = ctimes
			return dic

api.add_resource(close_json, '/listCloseOnly/json')

class close_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = User.verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('close_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['close_times'] + ", "
			return csv_string

api.add_resource(close_csv, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
