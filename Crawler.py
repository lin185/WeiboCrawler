# -*- coding: utf-8 -*-
import threading
import math
import os
import requests
import time
import random

import Logger as Logger

class Crawler:
	## Variables:

	cookies = []
	url_list = []
	folder_path = ""
	threads = []
	url_lock = threading.Lock()

	## Functions:

	# Constructor
	def __init__(self, url_list, cookies, keyword):

		self.url_list = url_list
		self.cookies = cookies

		num_of_cookies = len(self.cookies)
		# num_of_urls = len(self.url_list) # 10
		# urls_for_each_cookie = int(math.ceil(float(num_of_urls) / num_of_cookies))
		
		
		# create new folder to store crawl results
		current_time = time.localtime()
		timestr = time.strftime('%Y.%m.%d.%H.%M.%S', current_time)
		self.folder_path = "./"+timestr+"."+keyword
		os.makedirs(self.folder_path)

		# create threads
		for i in range(num_of_cookies):
			# urls = self.url_list[i:i+urls_for_each_cookie]
			# print i
			# for url in urls:
			# 	print url.decode('utf-8')
			# print "----------"
			self.threads.append( threading.Thread(target=self.crawl, args=(str(i))) ) 

		return


	def start(self):
		Logger.write("Crawler started.", 1)
		for t in self.threads:
			t.start()

		for t in self.threads:
			t.join()

		Logger.write("Crawler finished.", 1)
		return



	def crawl(self, cookie_id_str):
		# print "TODO: Crawl Implementation"
		thread_id = str(threading.current_thread().name)
		cookie_id = int(cookie_id_str)
		cookie = self.cookies[cookie_id]

		while 1:
			self.url_lock.acquire()
			if len(self.url_list) == 0:
				self.url_lock.release()
				return

			url = self.url_list.pop(0)
			self.url_lock.release()


			# extract param from url
			index1 = url.index("&timescope=custom:")+18
			index2 = url.index("&", index1)
			timescope = url[index1:index2].split(":")

			index1 = url.index("&region=custom:")+15
			index2 = url.index("&", index1)
			region = url[index1:index2].split(":")

			pagenum = 1
			while pagenum <= 50:
				final_url = url + "page=" + str(pagenum)
				Logger.write(thread_id + " <" + final_url + ">", 1)

				html = requests.get(final_url, cookies = cookie).content

				sleeptime = random.randint(10, 25)
				print thread_id, 'sleeps for ' + str(sleeptime) + ' seconds...'
				time.sleep(sleeptime)

				# check has next page
				if ('<div class=\\"pl_noresult\\">' in html) or ('<p class=\\"noresult_tit\\">' in html):
					# no search results
					break
				else:				
					filepath = self.folder_path + "/" + timescope[0]+"_"+timescope[1]+"_"+region[0]+"-"+region[1]+"_"+str(pagenum)+".html"
					with open(filepath, 'w') as f:
						f.write(html)

					if ('class=\\"page next S_txt1 S_line1\\">\\u4e0b\\u4e00\\u9875' in html):
						# has 下一页
						pagenum += 1
					else:
						# No 下一页
						break

		return


