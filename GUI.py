# -*- coding: utf-8 -*-
# Weibo Search GUI
#   Author: Binhao Lin


from Tkinter import *
from Login import Login
from datetime import datetime

from ProvinceCityConfig import ProvinceCityConfig
from Crawler import Crawler


def update_province_callback(currProvince):
    pid = pcconfig.getProvinceID(currProvince.decode('utf-8'))
    clist = pcconfig.getCitiesOfProvince(pid)
    m = cMenu.children['menu']
    m.delete(0, 'end')
    for city in clist:
        m.add_command(label=city, command=lambda temp = city: cMenu.setvar(cMenu.cget("textvariable"), value = temp))
    cList.set(clist[0])
    return


def search_callback():
    keyword = searchinput.get()
    time_from = timeinputfromText.get()
    time_to = timeinputtoText.get()
    province = pList.get()
    city = cList.get()

    # validate input
    if len(keyword) == 0:
        print "Input is empty"
        return

    if time_from == "YYYY-MM-DD":
        time_from = ""
    elif validate_date(time_from) == False:
        print "Time From format error."
        return
    if time_to == "YYYY-MM-DD":
        time_to = ""
    elif validate_date(time_to) == False:
        print "Time To format error."
        return
    
    url_list = GenerateURLs(keyword, time_from, time_to, province, city)

    crawler = Crawler(url_list, cookies)
    crawler.start()

    return




def GenerateURLs(keyword, time_from, time_to, province_name, city_name):
    # Without any specifications:
    #   http://s.weibo.com/weibo/lush&suball=1&Refer=g
    # With Time specification:
    #   http://s.weibo.com/weibo/%25E5%258D%2581%25E5%25AD%2597%25E6%259E%25B6&typeall=1&suball=1&timescope=custom:2016-10-05:&Refer=g
    #   http://s.weibo.com/weibo/%25E5%258D%2581%25E5%25AD%2597%25E6%259E%25B6&typeall=1&suball=1&timescope=custom::2016-10-10&Refer=g
    #   http://s.weibo.com/weibo/lush&typeall=1&suball=1&timescope=custom:2016-10-03:2016-10-05&Refer=g
    # With region (province only) specification:
    #   http://s.weibo.com/weibo/lush&region=custom:34:1000&typeall=1&suball=1&Refer=g
    # With region (both province and bity) specification:
    #   http://s.weibo.com/weibo/lush&region=custom:34:2&typeall=1&suball=1&Refer=g
    # With time and region specifications:
    #   http://s.weibo.com/weibo/lush&region=custom:34:2&typeall=1&suball=1&timescope=custom:2016-10-01:2016-10-12&Refer=g
    #   http://s.weibo.com/weibo/%25E5%258D%2581%25E5%25AD%2597%25E6%259E%25B6&region=custom:11:1&typeall=1&suball=1&timescope=custom:2015-10-07:2016-10-12&Refer=g
    #   http://s.weibo.com/weibo/%25E5%258D%2581%25E5%25AD%2597%25E6%259E%25B6&region=custom:11:1&typeall=1&suball=1&timescope=custom:2015-10-07:2016-10-12&page=2
    # print "GenerateURLs"

    url_list = []

    province_id = pcconfig.getProvinceID(province_name)
    city_id = pcconfig.getCityID(province_name, city_name)
    # print province_name, province_id
    # print city_name, city_id

    url = "http://s.weibo.com/weibo/"
    url += keyword + "&typeall=1" + "&suball=1"
    if len(time_from) > 0 and len(time_to) > 0:
        url += "&timescope=custom:" + time_from + ":" + time_to
    elif len(time_from) > 0:
        url += "&timescope=custom:" + time_from + ":"
    elif len(time_to) > 0:
        url += "&timescope=custom::" + time_to


    if province_id == '0': # all province
        for p in provinces:
            pid = pcconfig.getProvinceID(p.decode('utf-8'))
            if pid != '0':
                cities = pcconfig.getCitiesOfProvince(pid)
                for c in cities:
                    cid = pcconfig.getCityID(p.decode('utf-8'), c.decode('utf-8'))
                    if cid != '0' and cid != '1000':
                        print "(",pid, p.decode('utf-8'),")", "(",cid, c.decode('utf-8'),")"
                        url_list.append(url+"&region=custom:"+pid+":"+cid+"&")
    else:   # only one province
        if city_id == '0' or city_id == '1000': # all cities
            cities = pcconfig.getCitiesOfProvince(province_id)
            for c in cities:
                cid = pcconfig.getCityID(province_name, c.decode('utf-8'))
                if cid != '0' and cid != '1000':
                    print "(",province_id, province_name,")", "(",cid, c.decode('utf-8'),")"
                    url_list.append(url+"&region=custom:"+province_id+":"+cid+"&")
        else:   # one city
            print "(",province_id, province_name,")", "(",city_id, city_name,")"
            url_list.append(url+"&region=custom:"+province_id+":"+city_id+"&")

    return url_list



def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Auto login, get cookies

cookies = []
lines = open("./WeiboAccounts",'r').read().split('\n')
for line in lines:
    # skip those accounts that are commented out 
    if line.startswith("#"):
        continue
    info = line.split(' ')
    username = info[0]
    password = info[1]
    # print username, password
    # log in and get cookie
    user = Login(username, password)
    user.callLogin()
    cookies.append(user.cookie)


# Initialize Province and city lists
pcconfig = ProvinceCityConfig()
provinces = pcconfig.getProvinceList()
cities = [['城市/地区']]

# Construct the search GUI
root = Tk()
root.title("Weibo Search")
# root.geometry("400x100")

# search box
frame1 = Frame()
frame1.pack(fill=X)
searchlabel = Label(frame1, text="Search for: ")          
searchinput = Entry(frame1, width=45)

# time box
frame2 = Frame()
frame2.pack(fill=X)
timelabelfrom = Label(frame2, text="Time From: ")
timeinputfromText = StringVar()
timeinputfromText.set("YYYY-MM-DD")
timeinputfrom = Entry(frame2, width=20, textvariable=timeinputfromText)

timelabelto  = Label(frame2, text="To: ")
timeinputtoText = StringVar()
timeinputtoText.set("YYYY-MM-DD")
timeinputto = Entry(frame2, width=20, textvariable=timeinputtoText)

# province and city lists
frame3 = Frame()
frame3.pack(fill=X)
locationlabel = Label(frame3, text="Location: ")
pList = StringVar(value=provinces[0])
pMenu = OptionMenu(frame3, pList, *provinces, command=update_province_callback)
cList = StringVar(value=cities[0][0])
cMenu = OptionMenu(frame3, cList, *cities[0])

# search button
searchButton = Button(root, text="Search", command=search_callback)

# Set GUI visible
searchlabel.grid(row=0)
searchinput.grid(row=0, column=1)
timelabelfrom.grid(row=1, sticky=W)
timeinputfrom.grid(row=1, column=1, sticky=W)
timelabelto.grid(row=1, column=2, sticky=W)
timeinputto.grid(row=1, column=3, sticky=W)
locationlabel.grid(row=2)
pMenu.grid(row=2, column=1)
cMenu.grid(row=2, column=2)
searchButton.pack()

# start running
root.mainloop()
