import psutil
from tkinter import *
import threading

def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        inTarget = False
        try:
            name = psutil.Process(pid).name()
            inTarget = name in processname
        except:
            inTarget = False
        if inTarget:
            return True
                
    return False

status = "OFF"
def info():
    curStatus = "OFF"
    if judgeprocess(["soong_ui", "ninja"]):
        curStatus = "ON"
    else:
        curStatus = "OFF"
    
    def infoBox(info):
        win = Tk()
        win.title('NOTICE')
        win.configure(bg='white')
        win.overrideredirect(True)
        width = win.winfo_screenwidth()
        heigth = win.winfo_screenheight()
        windowWidth = win.winfo_width()
        windowHeight = win.winfo_height()
        win.geometry('+{}+{}'.format(int((width - windowWidth) / 2), int((heigth - windowHeight) / 2)))
        win.after(3000, win.destroy) 

        label = Label(win, text=info, bg='black', fg='red', font=('Monospace', 20),)
        label.pack()

        win.mainloop()

    global status
    if curStatus == "OFF" and status != curStatus:
        thread = threading.Thread(target=infoBox, args=("BUILD DONE",))
        thread.daemon = True
        thread.start()
    status = curStatus

    return status