from Tkinter import *
from Login import Login

'''
def update_agelist(currage):
    print currage

    menu = toption['menu']
    menu.delete(0, 'end')
    for age in range(int(currage), AGELIMIT):
        menu.add_command(label=age, command=Tkinter._setit(target, age))

    target.set(currage)

    return
'''


def login_callback():
    # print usernameInput.get()
    # print passwordInput.get()

    login_component = Login(usernameInput.get(), passwordInput.get())
    ret = login_component.login()

    
    if ret == 0:
        # ERROR
        return
    
    #print login_component.username
    #print login_component.password
    print "Login OK!"
    
    '''
    # loginFrame.destroy()
    
    frame1 = Frame()
    frame1.pack(fill=X)
            
    searchlabel = Label(frame1, text="Search for: ")          
    searchlabel.grid(row=1)
    searchinput = Entry(frame1, width=45)
    searchinput.grid(row=1, column=1)
    '''
    
    return





# root gui
root = Tk()
root.title("Weibo Search")
root.geometry("500x500")



# Login Frame
loginFrame = Frame()
loginFrame.pack(fill=X)
usernameLabel = Label(loginFrame, text="Username")  
usernameInput = Entry(loginFrame, width=25)
passwordLabel = Label(loginFrame, text="Password") 
passwordInput = Entry(loginFrame, show="*", width=25)
loginBotton = Button(loginFrame, text="Login", command=login_callback)
usernameLabel.grid(row=0, column=0)
usernameInput.grid(row=0, column=1)
passwordLabel.grid(row=0, column=2)
passwordInput.grid(row=0, column=3)
loginBotton.grid(row=0, column=4)



# search input box

'''
frame1 = Frame()
frame1.pack(fill=X)
        
searchlabel = Label(frame1, text="Search for: ")          
searchlabel.grid(row=0)
searchinput = Entry(frame1, width=45)
searchinput.grid(row=0, column=1)


frame2 = Frame()
frame2.pack(fill=X)
timelabelfrom = Label(frame2, text="Time From: ")
timelabelfrom.grid(row=1, sticky=W)
timeinputfromText = StringVar()
timeinputfromText.set("YYYY-MM-DD")
timeinputfrom = Entry(frame2, width=20, textvariable=timeinputfromText)
timeinputfrom.grid(row=1, column=1, sticky=W)




timelabelto  = Label(frame2, text="To: ")
timelabelto.grid(row=1, column=2, sticky=W)
timeinputtoText = StringVar()
timeinputtoText.set("YYYY-MM-DD")
timeinputto = Entry(frame2, width=20, textvariable=timeinputtoText)
timeinputto.grid(row=1, column=3, sticky=W)


frame3 = Frame()
frame3.pack(fill=X)
locationlabel = Label(frame3, text="Location: ")
locationlabel.grid(row=2)



frame4 = Frame()
frame4.pack(fill=X)
AGELIMIT = 95
AGEOPT = [str(i) for i in range(AGELIMIT)]
current = StringVar(value='0')
coption = OptionMenu(frame4, current, *AGEOPT, command=update_agelist)
coption.grid(row=3)
'''


'''
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

w = apply(OptionMenu, (root, variable) + tuple(OPTIONS))
w.pack()
'''


root.mainloop()
