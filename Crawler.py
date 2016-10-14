# -*- coding: utf-8 -*-
from multiprocessing import Process
import math
import os
import requests
import time
import random
from Login import Login
# import io


class Crawler:
	## Variables:
	# cookies = [
	# "<RequestsCookieJar[<Cookie ALF=1507959144 for .weibo.com/>, <Cookie SCF=Av_i6pIeWu7pXrCjCXAEWtBT-CvnpN3HJ_ulcjl2r6VW5KSMGYOvDG7p_Cd81VBMZc5eEi6njE61AXKfr844C1w. for .weibo.com/>, <Cookie SUB=_2A251BB25DeTxGeBO6FEZ8SnIyziIHXVWcAhxrDV8PUNbktAKLWP6kW8V37rj_xVCxV5NE1ZKnqxiaIZ3Lw.. for .weibo.com/>, <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWx3d3rsYOkoaiZVLzjh97_5JpX5K2hUgL.Foq7e0eReKMXehB2dJLoI0qLxK-L1K5L12-LxK.L1KMLB.zLxKnLBoqL12zLxK-L1K5L12-LxKqL12zLBK.LxKqL12zLB-et for .weibo.com/>, <Cookie SUHB=0KAxeciWpSR_14 for .weibo.com/>, <Cookie TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517 for weibo.com/>]>",
	# "<RequestsCookieJar[<Cookie ALF=1507959152 for .weibo.com/>, <Cookie SCF=Av_i6pIeWu7pXrCjCXAEWtBT-CvnpN3HJ_ulcjl2r6VWF1yDPIW9AWdVQ4G7NOgV5zZXYX-ZNRZ79DJjsrj0jCM. for .weibo.com/>, <Cookie SUB=_2A251BB2hDeTxGeBO6FEZ8SnIyjqIHXVWcAhprDV8PUNbktANLVSjkW-eP6LBaWev4TjvLhaAWjwq-E6yHA.. for .weibo.com/>, <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5v9vCVsK0Xv5h9SkIia2E05JpX5K2hUgL.Foq7e0eReKMXeKq2dJLoIEXLxKML1h.L1-zLxKqL1K-LBoBLxKqL1h2LBKnLxKML1h.L1-zLxK-L1hnLBKBt for .weibo.com/>, <Cookie SUHB=0IIV6XBhQiSqic for .weibo.com/>, <Cookie TC-Ugrow-G0=e66b2e50a7e7f417f6cc12eec600f517 for weibo.com/>]>",
	# "<RequestsCookieJar[<Cookie ALF=1507959159 for .weibo.com/>, <Cookie SCF=Av_i6pIeWu7pXrCjCXAEWtBT-CvnpN3HJ_ulcjl2r6VWjrl8nnqIPtodJx82Z8hLcfxM8Bqg4WoNPrgskiFjoYQ. for .weibo.com/>, <Cookie SUB=_2A251BB2nDeTxGeBO6FYQ8C3NyT6IHXVWcAhvrDV8PUNbktANLRXFkW9qTP3uZF7HmMIx9n1eEI9zMdIoww.. for .weibo.com/>, <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhK7NOE02o46NfzjpBWGas65JpX5K2hUgL.Foq7e0Bpehepeoz2dJLoIEBLxKMLB.2LB-2LxK-LB--L1h2LxKML1hzL12-LxKMLB.2LB-2t for .weibo.com/>, <Cookie SUHB=0rr71802lb04S9 for .weibo.com/>, <Cookie TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456 for weibo.com/>]>"
	# ]

	cookies = []
	url_list = []
	
	# url_list = [
	# "http://s.weibo.com/weibo/十字架&region=custom:44:1&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 6 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:2&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 1 page
	# "http://s.weibo.com/weibo/十字架&region=custom:44:3&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 5 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:4&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 1 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:5&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 1 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:6&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 3 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:7&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 2 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:8&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 1 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:9&typeall=1&suball=1&timescope=custom:2016-08-01:2016-10-01",# 1 pages
	# "http://s.weibo.com/weibo/十字架&region=custom:44:51&typeall=1&suball=1&timescope=custom:2016-10-01:2016-10-01"# 0 page
	# ]

	folder_path = ""
	## Functions:

	# Constructor
	def __init__(self, url_list, cookies):
		# print "TODO: Crawler Initialization"

		self.url_list = url_list
		self.cookies = cookies

		num_of_cookies = len(self.cookies) # 3
		num_of_urls = len(self.url_list) # 10
		urls_for_each_cookie = int(math.ceil(float(num_of_urls) / num_of_cookies))
		count = 0
		processes = []

		current_time = time.localtime()
		timestr = time.strftime('%Y.%m.%d.%H.%M.%S', current_time)
		self.folder_path = "./"+timestr
		os.makedirs(self.folder_path)

		for i in xrange(0,num_of_urls,urls_for_each_cookie):
			urls = self.url_list[i:i+urls_for_each_cookie]
			# print i
			# for url in urls:
			# 	print url.decode('utf-8')
			# print "----------"
			processes.append( Process(target=self.crawl, args=(urls, self.cookies[count])) )
			count += 1

		for p in processes:
			p.start()

		for p in processes:
			p.join()

		print "done"
		return



	def crawl(self, urls, cookie):
		# print "TODO: Crawl Implementation"
		# print os.getpid()
		process_id = os.getpid()


		# cookie = {"Cookie": cookie}
		i = 0
		for url in urls:
			index1 = url.index("&region=custom:")+15
			index2 = url.index("&", index1)
			region = url[index1:index2].split(":")
			# print region
			# print cookie
			print "Process", process_id, "is downloading page", region
			html = requests.get(url, cookies = cookie).content
			filepath = self.folder_path + "/" + region[0]+"-"+region[1]
			# print process_id
			# print filepath
			# print html
			with open(filepath, 'w') as f:
				f.write(html)

			interval = 40
			sleeptime_one = random.randint(interval-25, interval-15)
			sleeptime_two = random.randint(interval-15, interval)
			if i%2 == 0:
				sleeptime = sleeptime_two
			else:
				sleeptime = sleeptime_one
			print "Process", process_id, 'sleeps ' + str(sleeptime) + ' seconds...'
			time.sleep(sleeptime)
			i += 1

		# for i in range(startpage, endpage+1):
  #       print "Download page ",i,"..."
  #       # url + page number
  #       newurl = url + str(i);
  #       print newurl

  #       # get page
  #       html = requests.get(newurl, cookies = cookie).content

  #       # write
  #       filename = "./query/page"+str(i).zfill(2)
  #       f = open(filename, "w+")
  #       f.write(html)
  #       f.close()

  #       # robot protection - sleep a while
  #       interval = 50
  #       sleeptime_one = random.randint(interval-25, interval-15)
  #       sleeptime_two = random.randint(interval-15, interval)
  #       if i%2 == 0:
  #           sleeptime = sleeptime_two
  #       else:
  #           sleeptime = sleeptime_one
  #       print 'sleeping ' + str(sleeptime) + ' seconds...'
  #       time.sleep(sleeptime)

		return






# test


# c = Crawler()