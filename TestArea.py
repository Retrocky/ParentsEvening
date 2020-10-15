from tkinter import Tk  # Used to hide the default tkinter dialog box when choosing a file
import tkinter.filedialog as fd  # Used to browse files
import os  # Used to access the current directory


def getFile():
    Tk().withdraw()
    return fd.askopenfilename(initialdir=os.getcwd(), title="Select CSV to import",
                              filetypes=(('CSV files', '*.csv'), ('all files', '*.*')))


while True:
    print(getFile())
