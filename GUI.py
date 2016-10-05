# Weibo Search GUI
#   Author: Binhao Lin

from Tkinter import *
from Login import Login


provinces = ['All', 'Beijing', 'Zhejiang', 'Shanghai']
cities = [['All'], ['Chaoyang', 'Xuanwu'], ['Wenzhou', 'Hangzhou'], ['Xuhui', 'Pudong']]


def update_province(currProvince):
    print currProvince
    index = provinces.index(currProvince)
    print index
    clist = cities[index]
    m = cMenu.children['menu']
    m.delete(0, 'end')
    for city in clist:
        m.add_command(label=city, command=lambda temp = city: cMenu.setvar(cMenu.cget("textvariable"), value = temp))
    return



def login_callback():
    # Try login
    login_component = Login(usernameInput.get(), passwordInput.get())
    ret = login_component.login()
    ret = 1

        
    # Check if login failed
    if ret == 0:
        # ERROR
        print "Login ERROR!"
        return

    # Set search GUI visible
    loginFrame.destroy()
    msg.pack()  
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
    return


def search_callback():

    return



# root gui
root = Tk()
root.title("Weibo Search")
root.geometry("400x150")


# Login Frame - visible 
loginFrame = Frame()
loginFrame.pack(fill=X)
usernameLabel = Label(loginFrame, text="Username")  
usernameInput = Entry(loginFrame, width=25)
passwordLabel = Label(loginFrame, text="Password") 
passwordInput = Entry(loginFrame, show="*", width=25)
loginBotton = Button(loginFrame, text="Login", command=login_callback)
usernameLabel.grid(row=0, column=0)
usernameInput.grid(row=0, column=1)
passwordLabel.grid(row=1, column=0)
passwordInput.grid(row=1, column=1)
loginBotton.grid(row=2, column=0)




# Construct the search GUI
# Search GUI - invisible initailize, only visible after successfully logged in

msgFrame = Frame()
msgFrame.pack(fill=X)
msg = Label(msgFrame, text="Login Successful!")
#msg.pack()  


frame1 = Frame()
frame1.pack(fill=X)
searchlabel = Label(frame1, text="Search for: ")          
searchinput = Entry(frame1, width=45)
#searchlabel.grid(row=0)
#searchinput.grid(row=0, column=1)


frame2 = Frame()
frame2.pack(fill=X)
timelabelfrom = Label(frame2, text="Time From: ")
timeinputfromText = StringVar()
timeinputfromText.set("YYYY-MM-DD")
timeinputfrom = Entry(frame2, width=20, textvariable=timeinputfromText)
#timelabelfrom.grid(row=1, sticky=W)
#timeinputfrom.grid(row=1, column=1, sticky=W)

timelabelto  = Label(frame2, text="To: ")
timeinputtoText = StringVar()
timeinputtoText.set("YYYY-MM-DD")
timeinputto = Entry(frame2, width=20, textvariable=timeinputtoText)
#timelabelto.grid(row=1, column=2, sticky=W)
#timeinputto.grid(row=1, column=3, sticky=W)


frame3 = Frame()
frame3.pack(fill=X)
locationlabel = Label(frame3, text="Location: ")
pList = StringVar(value=provinces[0])
pMenu = OptionMenu(frame3, pList, *provinces, command=update_province)
cList = StringVar(value=cities[0][0])
cMenu = OptionMenu(frame3, cList, *cities[0])
#locationlabel.grid(row=2)
#pMenu.grid(row=2, column=1)
#cMenu.grid(row=2, column=2)

searchButton = Button(root, text="Search", command=search_callback)
#searchButton.pack()

root.mainloop()
