# Weibo Search GUI
#   Author: Binhao Lin

from Tkinter import *
from Login import Login
from datetime import datetime


provinces = ['All', 'Beijing', 'Zhejiang', 'Shanghai']
cities = [['All'], ['Chaoyang', 'Xuanwu'], ['Wenzhou', 'Hangzhou'], ['Xuhui', 'Pudong']]


def update_province(currProvince):
    index = provinces.index(currProvince)
    clist = cities[index]
    m = cMenu.children['menu']
    m.delete(0, 'end')
    for city in clist:
        m.add_command(label=city, command=lambda temp = city: cMenu.setvar(cMenu.cget("textvariable"), value = temp))
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
    province = pList.get()
    city = cList.get()

    # validate input
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

# Construct the search GUI
root = Tk()
root.title("Weibo Search")
root.geometry("400x100")

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
