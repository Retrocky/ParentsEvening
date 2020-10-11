'''
from tkinter import *

def clickedExit():
    notClicked = False

notClicked = True

window = Tk()
window.title('Parents Evening')
#window.geometry('300x300')
window.resizable(0,0)

if notClicked == True:
    button1 = Button(window,text = 'Run')
    button1.grid(row=1,column=1,columnspan=3)

if notClicked == False:
    button1 = Button(window,text='oof')

button2 = Button(window,text = 'Configure')
button2.grid(row=2,column=1,columnspan=3)

button3 = Button(window,text = 'Exit',command=clickedExit)
button3.grid(row=3,column=1,columnspan=3)

welcomeText = Label(window,text='Parents evening scheduler')
welcomeText.grid(row=0,column=1,columnspan=5)

window.mainloop()
'''

a,b = []
a.append('lol')
b.append('ok')