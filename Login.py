#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Required
- requests (必须)
- rsa (必须)
- pillow (可选)
'''
import time
import base64
import rsa
import binascii
<<<<<<< HEAD
import requests
import re
import random
try:
    from PIL import Image
except:
    pass
try:
    from urllib.parse import quote_plus
except:
    from urllib import quote_plus

'''
如果没有开启登录保护，不用输入验证码就可以登录
如果开启登录保护，需要输入验证码
'''


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:41.0) Gecko/20100101 Firefox/41.0'
headers = {
    'User-Agent': agent
}

session = requests.session()

# 访问 初始页面带上 cookie
index_url = "http://weibo.com/login.php"
try:
    session.get(index_url, headers=headers, timeout=2)
except:
    session.get(index_url, headers=headers)
try:
    input = raw_input
except:
    pass

def get_su(username):
    """
    对 email 地址和手机号码 先 javascript 中 encodeURIComponent
    对应 Python 3 中的是 urllib.parse.quote_plus
    然后在 base64 加密后decode
    """
    username_quote = quote_plus(username)
    username_base64 = base64.b64encode(username_quote.encode("utf-8"))
    return username_base64.decode("utf-8")


# 预登陆获得 servertime, nonce, pubkey, rsakv
def get_server_data(su):
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su="
    pre_url = pre_url + su + "&rsakt=mod&checkpin=1&client=ssologin.js(v1.4.18)&_="
    pre_url = pre_url + str(int(time.time() * 1000))
    pre_data_res = session.get(pre_url, headers=headers)

    sever_data = eval(pre_data_res.content.decode("utf-8").replace("sinaSSOController.preloginCallBack", ''))

    return sever_data


# print(sever_data)


def get_password(password, servertime, nonce, pubkey):
    rsaPublickey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPublickey, 65537)  # 创建公钥
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  # 拼接明文js加密文件中得到
    message = message.encode("utf-8")
    passwd = rsa.encrypt(message, key)  # 加密
    passwd = binascii.b2a_hex(passwd)  # 将加密信息转换为16进制。
    return passwd


def get_cha(pcid):
    cha_url = "http://login.sina.com.cn/cgi/pin.php?r="
    cha_url = cha_url + str(int(random.random() * 100000000)) + "&s=0&p="
    cha_url = cha_url + pcid
    cha_page = session.get(cha_url, headers=headers)
    with open("cha.jpg", 'wb') as f:
        f.write(cha_page.content)
        f.close()
    try:
        im = Image.open("cha.jpg")
        im.show()
        im.close()
    except:
        print(u"请到当前目录下，找到验证码后输入")


def login(username, password):
    # su 是加密后的用户名
    su = get_su(username)
    sever_data = get_server_data(su)
    servertime = sever_data["servertime"]
    nonce = sever_data['nonce']
    rsakv = sever_data["rsakv"]
    pubkey = sever_data["pubkey"]
    showpin = sever_data["showpin"]
    password_secret = get_password(password, servertime, nonce, pubkey)
    vflag = 0
    if sever_data.__len__() > 9:
        vflag = 1


    # -- Hanye -- 10/12/2016
    # the setting below result in http://passport.weibo.com/wbsso/login? XXX
    # It is a iframe form of login
    '''postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'useticket': '1',
        'pagerefer': "http://login.sina.com.cn/sso/logout.php?entry=miniblog&r=http%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl",
        'vsnf': '1',
        'su': su,
        'service': 'miniblog',
        'servertime': servertime,
        'nonce': nonce,
        'pwencode': 'rsa2',
        'rsakv': rsakv,
        'sp': password_secret,
        'sr': '1366*768',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
        }'''

    postdata = {'entry': 'weibo',
		'gateway': '1',
		'from': '',
		'savestate': '7',
		'userticket': '1',
		'ssosimplelogin': '1',
		'vsnf': '1',
		'vsnval': '',
		'su': su,
		'service': 'miniblog',
		'servertime': servertime,
		'nonce': nonce,
		'pwencode': 'rsa2',
		'sp': password_secret,
		'encoding': 'UTF-8',
		'prelt': '115',
		'rsakv' : rsakv,
		'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
		'returntype': 'META'
	    }
    #login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)'
    login_url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)'
    #if showpin == 0:
    #    login_page = session.post(login_url, data=postdata, headers=headers)
    #else:
    # showpin is always 0, so do not use showpin
    if vflag == 0:
        login_page = session.post(login_url, data=postdata, headers=headers)
        #html = requests.post(login_url,data=postdata).content
    else:
        pcid = sever_data["pcid"]
        get_cha(pcid)
        postdata['door'] = input(u"请输入验证码")
        login_page = session.post(login_url, data=postdata, headers=headers)

    newlogin_page = login_page.content
    urltemp = re.findall('location.replace\(\'(.*?)\'',newlogin_page,re.S)
    #print(urltemp)
    if(len(urltemp) == 0):
        print("login failed")
        return
    else:
        urlnew = urltemp[0]
        cookies = requests.get(urlnew).cookies
        #print(cookies)
        return cookies
    #login_loop = (login_page.content.decode("GBK"))
    # print(login_loop)
    #pa = r'location\.replace\([\'"](.*?)[\'"]\)'
    #loop_url = re.findall(pa, login_loop)[0]
    # print(loop_url)
    #login_index = session.get(loop_url, headers=headers)
    #cookies = session.get(loop_url).cookies
    #print(cookies)
    '''uuid = login_index.text
    uuid_pa = r'"uniqueid":"(.*?)"'
    print uuid
    uuid_res = re.findall(uuid_pa, uuid, re.S)[0]
    web_weibo_url = "http://weibo.com/%s/profile?topnav=1&wvr=6&is_all=1" % uuid_res
    weibo_page = session.get(web_weibo_url, headers=headers)
    weibo_pa = r'<title>(.*?)</title>'
    # print(weibo_page.content.decode("utf-8"))
    userID = re.findall(weibo_pa, weibo_page.content.decode("utf-8", 'ignore'), re.S)[0]
    print(u"欢迎你 %s, 登录微博" % userID)'''

class Login():

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cookie = ""


    def callLogin(self):
        self.cookie = login(self.username, self.password)


    '''if __name__ == "__main__":
    username = input(u'用户名：')
    password = input(u'密码：')
    #username = "*****"
    #password = "*****"
    login(username, password)'''



user1 = Login("17192006343","q1314120")
user1.callLogin()
print(user1.cookie)

user2 = Login("17191631495","a123456")
user2.callLogin()
print(user2.cookie)

user3 = Login("17192006340","q1314120")
user3.callLogin()
print(user3.cookie)
=======
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






>>>>>>> origin/master
