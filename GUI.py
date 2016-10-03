from Tkinter import *



def update_agelist(currage):
    print currage
    '''
    menu = toption['menu']
    menu.delete(0, 'end')
    for age in range(int(currage), AGELIMIT):
        menu.add_command(label=age, command=Tkinter._setit(target, age))

    target.set(currage)
    '''
    return



# root gui
root = Tk()
root.title("Weibo Search")
root.geometry("500x500")

# search input box
'''
searchlabel = Label(root, text="Search for: ")
searchlabel.pack(padx=5, pady=10, side=LEFT)
searchbox = Text(root, height=1, width=50)
searchbox.pack(padx=5, pady=10, side=LEFT)

timelabel = Label(root, text="Time From: ")
timelabel.pack()
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
variable = StringVar(root)
variable.set(OPTIONS[0]) # default value

w = apply(OptionMenu, (root, variable) + tuple(OPTIONS))
w.pack()
'''


root.mainloop()
