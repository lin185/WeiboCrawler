# 1. Open Google Chrome
# 2. shift + ctrl + i
# 3. Go to Network, then check Preserve log
# 4. Enter the url: m.weibo.cn
# 5. Enter your username and password to login
# 6. On the right hand side, find the entry with name m.weibo.com
# 7. The field Cookie is what we need

class Login:
	## Variables:

	username = ""
	password = ""
	cookie = ""

	# other variables 


	## Functions:

	# Login Consturctor
	def __init__(self, username, password):
		self.username = username
		self.password = password


	# Actual Login function
	#	Use the username and password to log into weibo, and get the cookie
	#	Return 0 if login failed
	#	Return 1 if login succeed, also set the cookie
	def login(self):
		print "TODO: Login.py Implementation."


		return 0

	# Other functions you may need