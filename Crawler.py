# -*- coding: utf-8 -*-
import threading
import math
import os
import requests
import time
import random


class Crawler:
	## Variables:

	cookies = []
	url_list = []
	folder_path = ""
	threads = []

	## Functions:

	# Constructor
	def __init__(self, url_list, cookies):

		self.url_list = url_list
		self.cookies = cookies

		num_of_cookies = len(self.cookies) # 3
		num_of_urls = len(self.url_list) # 10
		urls_for_each_cookie = int(math.ceil(float(num_of_urls) / num_of_cookies))
		count = 0
		
		current_time = time.localtime()
		timestr = time.strftime('%Y.%m.%d.%H.%M.%S', current_time)
		self.folder_path = "./"+timestr
		os.makedirs(self.folder_path)

		# create threads
		for i in xrange(0,num_of_urls,urls_for_each_cookie):
			urls = self.url_list[i:i+urls_for_each_cookie]
			# print i
			# for url in urls:
			# 	print url.decode('utf-8')
			# print "----------"
			self.threads.append( threading.Thread(target=self.crawl, args=(urls, self.cookies[count])) )
			count += 1

		return


	def start(self):
		for t in self.threads:
			t.start()

		for t in self.threads:
			t.join()

		print "Done."

		return



	def crawl(self, urls, cookie):
		# print "TODO: Crawl Implementation"
		thread_id = threading.current_thread()
	
		i = 0
		for url in urls:
			# figure out how many pages
			html = requests.get(url, cookies = cookie).content
			num_pages = getNumOfPages(html)





			index1 = url.index("&region=custom:")+15
			index2 = url.index("&", index1)
			region = url[index1:index2].split(":")
			# print region
			# print cookie
			print thread_id, "is downloading page", region
			html = requests.get(url, cookies = cookie).content
			filepath = self.folder_path + "/" + region[0]+"-"+region[1]
			# print process_id
			# print filepath
			# print html
			with open(filepath, 'w') as f:
				f.write(html)

			interval = 30
			sleeptime_one = random.randint(interval-25, interval-15)
			sleeptime_two = random.randint(interval-15, interval)
			if i%2 == 0:
				sleeptime = sleeptime_two
			else:
				sleeptime = sleeptime_one
			print thread_id, 'sleeps ' + str(sleeptime) + ' seconds...'
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



# input a weibo search raw html content
# output how many pages need to crawl
def getNumOfPages(html):


	return