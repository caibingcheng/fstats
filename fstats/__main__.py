from asyncio import constants
from time import sleep
from tkinter import *
import threading
import psutil


def diskStats():
    return psutil.disk_usage('/')


def cpuStats():
    return psutil.cpu_percent(interval=1)


def memStats():
    return psutil.virtual_memory().percent


def winCreate():
    win = Tk()
    win.title('fstats')
    win.configure(bg='white')
    win.overrideredirect(True)

    width = win.winfo_screenwidth()
    heigth = win.winfo_screenheight()

    win.attributes('-type', 'black')
    win.attributes('-zoomed', False)
    win.attributes('-alpha', '0.8')
    win.attributes('-topmost', True)
    win.geometry('96x48+{}+{}'.format(width - 96 - 50, heigth - 48 - 50))
    win.resizable(width=0, height=0)

    def StartMove(event):
        win.x = event.x
        win.y = event.y

    def StopMove(event):
        win.x = None
        win.y = None

    def OnMotion(event):
        deltax = event.x - win.x
        deltay = event.y - win.y
        x = win.winfo_x() + deltax
        y = win.winfo_y() + deltay
        win.geometry("+%s+%s" % (x, y))

    win.bind("<ButtonPress-1>", StartMove)
    win.bind("<ButtonRelease-1>", StopMove)
    win.bind("<B1-Motion>", OnMotion)

    menu = Menu(win)

    def destroy():
        win.destroy()
    menu.add_command(label='退出', command=destroy)
    menu.add_command(label='取消')

    def popupmenu(event):
        menu.post(event.x_root, event.y_root)

    win.bind("<ButtonPress-3>", popupmenu)

    return win

config = {
    'high' : ['red', 'white'],
    'mid': ['white', 'black'],
    'low': ['white', 'black'], # ['green', 'white'],
}

def departLevel(cpu, mem):
    if (cpu > 90 or mem > 90):
        return 'high'
    if (cpu < 20 and mem < 30):
        return 'low'
    return 'mid'

def intervalProcess(win):
    textvariable = StringVar()

    label = Label(win, justify='left', anchor='w', bg='white', fg='black', cursor='fleur',
                  width=win.winfo_screenwidth(), height=win.winfo_screenheight(),
                  textvariable=textvariable)
    label.pack(padx=0, pady=0)

    def refresh(textvariable):
        while True:
            cpu = cpuStats()
            mem = memStats()
            info = " {:<6}{:<5}%\n {:<5}{:<5}%".format(
                "CPU:", cpu, "MEM:", mem)
            configLevel = config[departLevel(cpu, mem)]
            label['bg'] = configLevel[0]
            label['fg'] = configLevel[1]
            textvariable.set(info)
            sleep(1)

    thread = threading.Thread(target=refresh, args=(textvariable,))
    thread.daemon = True
    thread.start()


def main():
    win = winCreate()
    intervalProcess(win)
    win.mainloop()


if __name__ == '__main__':
    main()
