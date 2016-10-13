# -*- coding: utf-8 -*-
# Weibo Search GUI
#   Author: Binhao Lin


from Tkinter import *
from Login import Login
from datetime import datetime

from ProvinceCityConfig import ProvinceCityConfig


#provinces = ['All', 'Beijing', 'Zhejiang', 'Shanghai']
#cities = [['All'], ['Chaoyang', 'Xuanwu'], ['Wenzhou', 'Hangzhou'], ['Xuhui', 'Pudong']]


def update_province(currProvince):
    pid = pcconfig.getProvinceID(currProvince)
    clist = pcconfig.getCitiesOfProvince(pid)
    m = cMenu.children['menu']
    m.delete(0, 'end')
    for city in clist:
        m.add_command(label=city, command=lambda temp = city: cMenu.setvar(cMenu.cget("textvariable"), value = temp))
    cList.set(clist[0])


    # print pid, pcconfig.getProvinceName(pid)


    return



def login_callback():
    # Try login
    login_component = Login(usernameInput.get(), passwordInput.get())
    #ret = login_component.login()
    ret = 1

        
    # Check if login failed
    if ret == 0:
        # ERROR
        print "Login ERROR!"
        return

    # Set search GUI visible
    loginFrame.destroy()
    msg.pack()  
    
    return


def search_callback():
    keyword = searchinput.get().encode("utf-8")
    time_from = timeinputfromText.get()
    time_to = timeinputtoText.get()
    province = pList.get().encode("utf-8")
    city = cList.get().encode("utf-8")
    print province
    print city
    
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
    
    pid = pcconfig.getProvinceID(province_name)
    cid = pcconfig.getCityID(province_name, city_name)
    print province_name, pid
    print city_name, cid

    url = "http://s.weibo.com/weibo/"
    url += keyword + "&typeall=1" + "&suball=1"
    if len(time_from) > 0 and len(time_to) > 0:
        url += "&timescope=custom:" + time_from + ":" + time_to
    elif len(time_from) > 0:
        url += "&timescope=custom:" + time_from + ":"
    elif len(time_to) > 0:
        url += "&timescope=custom::" + time_to


    # if province_id == 0: # all province
    #     # list all the possibilities
    #     province_list = []
    #     for p in provinces:
    #         pid = pcconfig.getProvinceID(p)
    #         if pid != 0:
    #             province_list.add(pid)
    #             print p, pid

    # else:

    #     url += "&region=custom:" + province_id
    # print url



    return



def validate_date(d):
    try:
        datetime.strptime(d, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Auto login, get cookies
# t = Login();
# cookie = t.login("0017654187943","woshibh111")
# print cookie

cookies = ["<<class 'requests.cookies.RequestsCookieJar'>[<Cookie ALF=1507830797 for .weibo.com/>, <Cookie SCF=AmrMZ9utXGGnkPCEZA5_l3AnL9WgHGdWK98tr3fnog4m4Tq4DK-GY9P7AOaXsmz1WQiIu352x_DnihahiOSVx7w. for .weibo.com/>, <Cookie SUB=_2A256-gjeDeTxGeNH4lcT8SvFzT2IHXVZjn0WrDV8PUNbktANLWuskW8ZE7NnSiWVAhULa5iysywdoJ6sMQ.. for .weibo.com/>, <Cookie SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5_eRLFeSu7TG91QqTCvR8i5JpX5K2hUgL.Fo-41K-EeK-4So22dJLoI0.LxKnLBoMLB-qLxK-L12BLBK2LxKqL1KqLB-qLxKMLBK.LB.2LxKnL12BLBK2LxKnL12BLBK27eh-t for .weibo.com/>, <Cookie SUHB=0vJICjD2bB7C8h for .weibo.com/>, <Cookie TC-Ugrow-G0=0149286e34b004ccf8a0b99657f15013 for weibo.com/>]>"]
print cookies[0]


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
pMenu = OptionMenu(frame3, pList, *provinces, command=update_province)
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
