from psw import hash_password, verify_password

class User():
	def __init__(self,username,password):
		self.username = username
		self.password = password
		db2.users.insert_one({'username': self.username})
	
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