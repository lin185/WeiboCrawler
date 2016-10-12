# 1. Open Google Chrome
# 2. shift + ctrl + i
# 3. Go to Network, then check Preserve log
# 4. Enter the url: m.weibo.cn
# 5. Enter your username and password to login
# 6. On the right hand side, find the entry with name m.weibo.com
# 7. The field Cookie is what we need

import base64
import requests
import re
import rsa
import binascii
import time


class Login:
	## Variables:

	#username = ""
	#password = ""
	#cookie = ""

	# other variables 
	
	## Functions:

	# Login Consturctor
	def __init__(self):
		return



	# Actual Login function
	#	Use the username and password to log into weibo, and get the cookie
	#	Return 0 if login failed
	#	Return 1 if login succeed, also set the cookie
	def login(self, username, password):
		# print "TODO: Login.py Implementation."
		# print "Login.py gets cookie"
		
		# -- Hanye 10/05/2016
		# ref: http://m.blog.csdn.net/article/details?id=48396545
		# ref: http://www.jianshu.com/p/36a39ea71bfd

		# username = raw_input(u'Login Name:') # type in su and sp for testing
		# password = raw_input(u'Password:')

		url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)%'+username
		#url = http://login.sina.com.cn/sso/prelogin.phpentry=weibo&callback=sinaSSOController.preloginCallBack&su=yourusername&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.11)
		# print url
		html = requests.get(url).content
		# time.sleep(10)

		servertime = re.findall('"servertime":(.*?),',html,re.S)[0]
		nonce = re.findall('"nonce":"(.*?)"',html,re.S)[0]
		pubkey = re.findall('"pubkey":"(.*?)"',html,re.S)[0]
		rsakv = re.findall('"rsakv":"(.*?)"',html,re.S)[0]

		username = base64.b64encode(username)
		rsaPublickey = int(pubkey, 16)
		key = rsa.PublicKey(rsaPublickey, 65537)
		message = str(servertime) + '\t' + str(nonce) + '\n' + str(password) 

		passwd = rsa.encrypt(message, key)
		passwd = binascii.b2a_hex(passwd)

		login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'

		data = {'entry': 'weibo',
			'gateway': '1',
			'from': '',
			'savestate': '7',
			'userticket': '1',
			'ssosimplelogin': '1',
			'vsnf': '1',
			'vsnval': '',
			'su': username,
			'service': 'miniblog',
			'servertime': servertime,
			'nonce': nonce,
			'pwencode': 'rsa2',
			'sp': passwd,
			'encoding': 'UTF-8',
			'prelt': '115',
			'rsakv' : rsakv,
			'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
			'returntype': 'META'
	        }
		
		html = requests.post(login_url,data=data).content
		# print(html)
		urltemp = re.findall('location.replace\(\'(.*?)\'',html,re.S)
		if(len(urltemp) == 0):
			print("login failed")
			return 0
		else:
			urlnew = urltemp[0]
		#urlnew = re.findall('location.replace\(\'(.*?)\'',html,re.S)[0]
		cookies = requests.get(urlnew).cookies
		print(cookies)

		return cookies

	# Other functions you may need


# -- test code start here --
#t = Login("vera","xu");
#t.login();

# t = Login();

# temp = open('./WeiboAccounts','r').read().split('\n')
# for line in temp:
# 	info = line.split(' ')
# 	username = info[0]
# 	password = info[1]
# 	print username
# 	print password
# 	t.login(username, password)






