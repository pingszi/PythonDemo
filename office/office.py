from tkinter import Tk
from time import sleep
from tkinter.messagebox import showwarning
import win32com.client as win32


# **操控excel
warn = lambda app: showwarning(app, "Exit?")
RANGE = range(3, 8)


def excel():
    app = "Excel"
    xl = win32.gencache.EnsureDispatch("{}.Application".format(app))
    ss = xl.Workbooks.Add()
    sh = ss.ActiveSheet
    xl.Visible = True

    sleep(1)

    sh.Cells(1, 1).Value = "Python-to-{} Demo".format(app)
    sleep(1)
    for i in RANGE:
        sh.Cells(i, 1).Value = "Line {}".format(i)
        sleep(1)

    sh.Cells(i + 2, 1).Value = "Th-th-th-thats all folks!"

    warn(app)
    ss.close(False)
    xl.Application.Quit()

if __name__ == "__main__":
    Tk().withdraw()
    excel()



