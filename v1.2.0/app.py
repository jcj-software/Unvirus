import threading
import pickle

import tkinter as tk
import ttkbootstrap as tbs
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import *
from tkinter.ttk import *

from lib.core import *
from lib.lang import *
from lib.toggle import *
from lib.monitor import *

import pystray
import PIL.Image as Img
from pystray import MenuItem, Menu


def quit_window(icon: pystray.Icon):
    if setting['monitor'] == True:
        m.stop = True
    icon.stop()
    root.destroy()


def show_window():
    root.deiconify()


def on_exit():
    root.withdraw()
    
def theme(themeName):
    style.theme_use(themeName)
    with open('theme.dat', 'wb') as f:
        pickle.dump(themeName, f)

try:
    with open('theme.dat', 'rb') as f:
        style = tbs.Style(theme = pickle.load(f))
except:
    style = tbs.Style(theme = "litera")

root = style.master
root.title("Unvirus-1")
root.geometry("400x300")
root.iconbitmap('assets/icon.ico')
root.protocol('WM_DELETE_WINDOW', on_exit)
menu = (MenuItem(lang_load.lang_Show, show_window, default=True),
        Menu.SEPARATOR, MenuItem(lang_load.lang_Exit, quit_window))
image = Img.open("assets/icon.ico")
icon = pystray.Icon("icon", image, "Unvirus", menu)


def openFileFunc():
    filename = askopenfilename()
    filePath.delete(0, len(filePath.get()))
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

def monitorToolFunc():
    if monitorVar == 1:
        setting['monitor'] = True
    elif monitorVar == 0:
        setting['monitor'] = False
    with open('setting.dat', 'wb') as f:
        pickle.dump(setting, f)
        
def startToolFunc():
    if startVar == 1:
        setting['startup'] = True
    elif startVar == 0:
        setting['startup'] = False
    with open('setting.dat', 'wb') as f:
        pickle.dump(setting, f)

# Menubar Loading
menubar = tk.Menu(root)
Language = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '语言(Language)', menu = Language)
Language.add_command(label = 'English', command = lang_load._switchEnglish)
Language.add_command(label = '中文', command = lang_load._switchChinese)
Theme = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '主题(Themes)', menu = Theme)
Theme.add_command(label = 'Default', command = lambda: theme("litera"))
Theme.add_command(label = 'Cosmo', command = lambda: theme("cosmo"))
Theme.add_command(label = 'Flatly', command = lambda: theme("flatly"))
Theme.add_command(label = 'Journal', command = lambda: theme("journal"))
Theme.add_command(label = 'Lumen', command = lambda: theme("lumen"))
Theme.add_command(label = 'Minty', command = lambda: theme("minty"))
Theme.add_command(label = 'Pulse', command = lambda: theme("pulse"))
Theme.add_command(label = 'Sandstone', command = lambda: theme("sandstone"))
Theme.add_command(label = 'United', command = lambda: theme("united"))
Theme.add_command(label = 'Yeti', command = lambda: theme("yeti"))
Theme.add_command(label = 'Morph', command = lambda: theme("morph"))
Theme.add_separator()
Theme.add_command(label = 'Darkly', command = lambda: theme("darkly"))
Theme.add_command(label = 'Cyborg', command = lambda: theme("cyborg"))
Theme.add_command(label = 'Superhero', command = lambda: theme("superhero"))
Theme.add_command(label = 'Solar', command = lambda: theme("solar"))

# Toggles Loading
ToggleFrame = Frame(root)
ToggleFrame.pack(side = "top")
monitorVar = IntVar()
if setting['monitor'] == True:
    monitorVar.set(1)
monitorTool = Checkbutton(ToggleFrame, text = lang_load.lang_Monitor, variable = monitorVar, style = 'Roundtoggle.Toolbutton', command = monitorToolFunc)
monitorTool.pack(side = "top")
startVar = IntVar()
if setting['startup'] == True:
    startVar.set(1)
startTool = Checkbutton(ToggleFrame, text = lang_load.lang_Start, variable = startVar, style = 'Roundtoggle.Toolbutton', command = startToolFunc)
startTool.pack(side = "top")

# Buttons Loading
ButtonFrame = Frame(root)
ButtonFrame.pack(side = "bottom")
openFile = Button(ButtonFrame, text = lang_load.lang_OpenFile, command = openFileFunc, style = "Outline.TButton")
openFile.pack(side = "left", padx = 25)
checkFile = Button(ButtonFrame, text = lang_load.lang_CheckFile, command = checkFileFunc, style = "Outline.TButton")
checkFile.pack(side = "right", padx = 25)

# File Path Loading
filePathFrame = Frame(root)
filePathFrame.pack(side = "bottom")
filePath = Entry(filePathFrame, width = 50)
filePath.pack()

threading.Thread(target = icon.run, daemon = True).start()
m = monitor()
m.stop = False
if setting['monitor'] == True:
    threading.Thread(target = m.monitor).start()
elif setting['monitor'] == False:
    m.stop = True
root.config(menu = menubar)
on_exit()
root.mainloop()