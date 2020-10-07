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

dict1 = {'Will':'Mr.Jeff (3), Mr.Walter (1), Ms.Gary (1), Ms.Onion (1)','Jeff':'ye'}
temp = dict1['Will'].split(',')
for teacher in temp:
    if 'Mr.Walter' in teacher:
        temp.pop(temp.index(teacher))
dict1['Will'] = (',').join(temp)
print(dict1)