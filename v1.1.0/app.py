import tkinter as tk
import threading
import pystray
from tkinter.filedialog import *
from tkinter.messagebox import *
from lib.core import *
from lib.lang import *
from lib.monitor import *
from lib.theme import *
from PIL import Image
from pystray import MenuItem, Menu
from ttkbootstrap import *
import os
import sys
import win32api
import win32con

def quit_window(icon: pystray.Icon):
    m.stop = True
    icon.stop()
    root.destroy()


def show_window():
    root.deiconify()


def on_exit():
    root.withdraw()


style = Style(theme = 'cosmo')
root = style.master
root.title("Unvirus-1")
root.geometry("400x300")
root.iconbitmap('assets/icon.ico')
root.protocol('WM_DELETE_WINDOW', on_exit)
menu = (MenuItem(lang_load.lang_Show, show_window, default=True),
        Menu.SEPARATOR, MenuItem(lang_load.lang_Exit, quit_window))
image = Image.open("assets/icon.ico")
icon = pystray.Icon("icon", image, "Unvirus", menu)


def openFileFunc():
    filename = askopenfilename()
    filePath.insert(0, filename)
    
def checkFileFunc():
    if CheckFile(filePath.get()) == True:
        askyn = askyesno('Unvirus', filePath.get() + '\n' + lang_load.lang_FileStatus + lang_load.lang_Malicious + '\n' + lang_load.lang_Process)
        if askyn == False:
            pass
        elif askyn == True:
            os.remove(filePath.get())
    else:
        showinfo('Unvirus', filePath.get() + '\n' + lang_load.lang_FileStatus + lang_load.lang_Undetected)

# Menubar Loading
menubar = tk.Menu(root)
Language = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '语言(Language)', menu = Language)
Language.add_command(label = 'English', command = lang_load._switchEnglish)
Language.add_command(label = '中文', command = lang_load._switchChinese)

# Buttons Loading
ButtonFrame = tk.Frame(root)
ButtonFrame.pack(side = "bottom")
openFile = tk.Button(ButtonFrame, text = lang_load.lang_OpenFile, command = openFileFunc)
openFile.pack(side = "left", padx = 25)
checkFile = tk.Button(ButtonFrame, text = lang_load.lang_CheckFile, command = checkFileFunc)
checkFile.pack(side = "right", padx = 25)

# File Path Loading
filePathFrame = tk.Frame(root)
filePathFrame.pack(side = "bottom")
filePath = tk.Entry(filePathFrame, width = 50)
filePath.pack()

threading.Thread(target = icon.run, daemon = True).start()
m = monitor()
m.stop = False
threading.Thread(target = m.monitor).start()
key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run', 0, win32con.KEY_ALL_ACCESS)
win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, sys.argv[0])
win32api.RegCloseKey(key)
root.config(menu = menubar)
on_exit()
root.mainloop()