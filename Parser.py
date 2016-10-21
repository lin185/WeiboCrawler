#-*-coding:utf8-*-

import os
import unicodecsv

class Parser:
	## Variables:
	folder_path = ""


	## Functions:

	# Constructor
	def __init__(self, folder_path):
		self.folder_path = folder_path
		return



	def parse(self, pcConfig):
		dirs = os.listdir(self.folder_path)

		csvfilename = self.folder_path + ".results.csv"
		csvfile = open(csvfilename, 'w')
		csvwriter = unicodecsv.writer(csvfile,encoding='utf-8-sig')

		for file in dirs:
			if file.startswith('.'):
				continue

			temp = file[:-5]
			temp = temp.split("_")
			temp = temp[2]
			temp = temp.split("-")
			province_name = pcConfig.getProvinceName(temp[0])
			# province_id = unicode(temp[0], "utf-8") 
			# print province_name
			city_name = pcConfig.getCityName(temp[0], temp[1])
			# city_id = unicode(temp[1], "utf-8") 
			# print city_name


			f = open(self.folder_path+"/"+file, "r");
			content = f.read()
			# print content
			f.close()

			# find feed_list, only one
			feed_list = ParseClass(content, "feed_lists W_texta", "<div", "<\/div")
			if len(feed_list) == 0:
				# the page doesn't have any feeds
				continue

			# find feeds, 16 of them
			feeds = ParseClass(feed_list[0], "WB_cardwrap S_bg2 clearfix", "<div", "<\/div")



			for feed in feeds:
				# username in chinese
				username = ParseClass(feed, "W_texta W_fb", "<a", "<\/a")
				name = extractField(username[0], "nick-name")
				name = name.decode('unicode-escape')
				# print name

				# user identification number
				userid = extractField(username[0], "usercard")
				userid = userid[userid.find('=')+1:userid.find('&')]

				# official verify
				verifystatus = ParseClass(feed, "approve_co", "<a", "<\/a")
				# individual verify
				if len(verifystatus) == 0:
					verifystatus = ParseClass(feed, "approve", "<a", "<\/a")

				if len(verifystatus) == 0:
					status = "none"
				else:
					status = extractField(verifystatus[0], "title")
					status = status.decode('unicode-escape')

				# post contents
				content = ParseClass(feed, "comment_txt", "<p", "<\/p")
				startindex = content[0].find(">") + 1
				endindex = content[0].find("<\/p", startindex)
				content = content[0][startindex:endindex]
				content = content.decode('unicode-escape')

				# post time and from
				time_from = ParseClass(feed, "feed_from W_textb", "<div", "<\/div")
				time_ = ParseClass(time_from[0], "feed_list_item_date", "<a", "<\/a")
				from_ = ParseClass(time_from[0], "nofollow", "<a", "<\/a")
				startindex = time_[0].find('>') + 1
				endindex = time_[0].find('<', startindex)
				time_ = time_[0][startindex:endindex]
				if len(from_) == 0:
					from_ = ""
				else:
					startindex = from_[0].find('>') + 1
					endindex = from_[0].find('<', startindex)
					from_ = from_[0][startindex:endindex]
					from_ = from_.decode('unicode-escape')


				# shoucang, zhuanfa, pinglun, dianzan
				stat = ParseClass(feed, "\"line S_line1", "<span", "<\/span")
				counts = []
				for i in range(1, 4):
					if stat[i].find('<em>') == -1:
						counts.append("0")
					else:
						startindex = stat[i].find('<em>')+4
						endindex = stat[i].find('<', startindex)
						if endindex <= startindex:
							counts.append("0")
						else:
							counts.append(stat[i][startindex: endindex])

				zhuanfa = counts[0]
				pinglun = counts[1]
				dianzan = counts[2]
			    
				csvwriter.writerow([name, userid, status, content, time_, from_, zhuanfa, pinglun, dianzan, province_name, city_name] )
	            # print name

        # break;


# find div with given class from the content 
# there may be many matchig divs
# return a list of all matchings
def ParseClass(content, class_tag, tag_start, tag_end):

    index = 0
    res = []

    while index != -1:
        index = content.find(class_tag, index)
        # can't find any class with given tag
        if index == -1:
            # print "No more class with tag: ",class_tag;
            break
        # print class_tag, "index ",index

        # find the begining of the div tag
        while content[index] != '<':
            index = index - 1;
        startindex = index;
        # print "start: ",startindex

        # find the ending of the div tag
        divct = 0
        while index != -1:
            i1 = content.find(tag_start, index)
            i2 = content.find(tag_end, index)
            # print i1, i2
            if i1 == -1 or i2 == -1:
                endindex = i2
                index = -1
                break;
            if i1 < i2:
                divct += 1
                index = i1+1
            else:
                divct -= 1
                index = i2+1
            # print divct

            if divct <= 0:
                endindex = i2
                break
        # print endindex
        while content[endindex] != '>':
            endindex += 1
        # print "end: ",endindex

        res.append(content[startindex:endindex])

        index = endindex + 1

    return res;


def extractField(content, fieldID):
    startindex = content.find(fieldID)
    if startindex == -1:
        return ""
    while content[startindex] != '"':
        startindex += 1

    endindex = content.find("\"", startindex+2)
    if endindex == -1:
        return ""
    # print startindex, endindex
    return content[startindex+1:endindex-1]




