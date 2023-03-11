import threading
import pickle
import time

import tkinter as tk
import ttkbootstrap as tbs
from tkinter.filedialog import *
from tkinter.messagebox import *

from lib.core import *
from lib.lang import *
from lib.monitor import *
from lib.scan import *

import pystray
import PIL.Image as Img
from pystray import MenuItem, Menu

import glob
import getpass
import sys
import pickle
import win32api
import win32con

from tkinter import *
from tkinter.ttk import *

try:
    with open('setting.dat', 'rb') as f:
        setting = pickle.load(f)
except:
    setting = {'monitor': True, 'startup': True}
    
try:
    with open('theme.dat', 'rb') as f:
        style = tbs.Style(theme = pickle.load(f))
except:
    style = tbs.Style(theme = "litera")
    
m = monitor()
m.stop = False
s = scan()
s.stop = False

if setting['monitor']:
    threading.Thread(target = m.monitor).start()
else:
    m.stop = True


key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, win32con.KEY_ALL_ACCESS)
if setting['startup']:
    win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, sys.argv[0])
else:
    win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, "")
    
def theme(themeName):
    style.theme_use(themeName)
    with open('theme.dat', 'wb') as f:
        pickle.dump(themeName, f)

def quit_window(icon: pystray.Icon):
    if setting['monitor'] == True:
        m.stop = True
    s.stop = True
    icon.stop()
    root.destroy()

def show_window():
    root.deiconify()

def on_exit():
    root.withdraw()
    
def openFileFunc():
    filename = askopenfilename()
    filePath.delete(0, "end")
    filePath.insert(0, filename)
    
def checkFileFunc():
    if CheckFile(filePath.get()) == True:
        askyn = askyesno('Unvirus', filePath.get() + '\n' + lang_load.lang_FileStatus + lang_load.lang_Malicious + '\n' + lang_load.lang_Process)
        if askyn == False:
            m.black.append(filePath.get())
            with open('black.dat', 'wb') as f:
                pickle.dump(m.black, f)
        elif askyn == True:
            os.remove(filePath.get())
    else:
        showinfo('Unvirus', filePath.get() + '\n' + lang_load.lang_FileStatus + lang_load.lang_Undetected)

def fullScanFunc():
    threading.Thread(target = lambda: s.scan(lambda: ProgressBar.stop())).start()
    ProgressBar.start(10)
    
def monitorToolFunc():
    if monitorVar.get() == 1:
        setting['monitor'] = True
        m.stop = False
        threading.Thread(target = m.monitor).start()
    elif monitorVar.get() == 0:
        setting['monitor'] = False
        m.stop = True
    with open('setting.dat', 'wb') as f:
        pickle.dump(setting, f)
        
def startToolFunc():
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, win32con.KEY_ALL_ACCESS)
    if startVar.get() == 1:
        setting['startup'] = True
        win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, sys.argv[0])
        win32api.RegCloseKey(key)
    elif startVar.get() == 0:
        setting['startup'] = False
        win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, "")
        win32api.RegCloseKey(key)
    with open('setting.dat', 'wb') as f:
        pickle.dump(setting, f)
    
def ClearTrashThread():
    for filename in glob.glob(r'C:/Users/' + getpass.getuser() + r'/AppData/Local/Temp/*.*'):
        try:
            os.remove(filename)
        except:
            pass
    for filename in glob.glob(r'C:/Users/' + getpass.getuser() + r'/Local Settings/Temp/*.*'):
        try:
            os.remove(filename)
        except:
            pass
    for filename in glob.glob(r'C:/Windows/Temp/*.*'):
        try:
            os.remove(filename)
        except:
            pass
    showinfo("Unvirus", lang_load.lang_ClearTrashOver)
    ProgressBar1.stop()
    
def ClearTrash():
    ProgressBar1.start(10)
    threading.Thread(target = ClearTrashThread).start()
    
root = style.master
root.title("Unvirus")
root.geometry("500x300")
root.iconbitmap('assets/icon.ico')
root.protocol('WM_DELETE_WINDOW', on_exit)
menu = (MenuItem(lang_load.lang_Show, show_window, default=True),
        MenuItem(lang_load.lang_Exit, quit_window))
image = Img.open("assets/icon.ico")
icon = pystray.Icon("icon", image, "Unvirus", menu)

# Menubar Loading
menubar = tk.Menu(root)
Language = tk.Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '语言(Language)', menu = Language)
Language.add_command(label = 'English(Take effect after restarting the software)', command = lambda: lang_load._switchEnglish(quit_window, icon))
Language.add_command(label = '中文(重启软件后生效)', command = lambda: lang_load._switchChinese(quit_window, icon))
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
ToggleFrame1 = Frame(root)
ToggleFrame1.pack(side = "top")
monitorVar = IntVar()
monitorVar.set(setting['monitor'])
monitorTool = Checkbutton(ToggleFrame1, text = lang_load.lang_Monitor, variable = monitorVar, style = 'Roundtoggle.Toolbutton', command = monitorToolFunc)
monitorTool.pack(side = "left")
startVar = IntVar()
startVar.set(setting['startup'])
startTool = Checkbutton(ToggleFrame1, text = lang_load.lang_Start, variable = startVar, style = 'Roundtoggle.Toolbutton', command = startToolFunc)
startTool.pack(side = "right")

Separator1 = Separator(root, orient = HORIZONTAL)
Separator1.pack(side = "top", padx = 10, pady = 3, fill = X)

# Full Scan Loading
fullScanFrame = Frame(root)
fullScanFrame.pack(side = "bottom", pady = 10)
ProgressBar = Progressbar(fullScanFrame, orient = HORIZONTAL, length = 350, mode = 'indeterminate')
ProgressBar.pack()
fullScan = Button(fullScanFrame, text = lang_load.lang_Full, command = fullScanFunc, style = "Outline.TButton")
fullScan.pack(padx = 25)

Separator2 = Separator(root, orient = HORIZONTAL)
Separator2.pack(side = "bottom", padx = 10, pady = 3, fill = X)

# Sigle File Scanning Loading
SingleFileScanningFrame = Frame(root)
SingleFileScanningFrame.pack(side = "bottom", pady = 10)
filePath = Entry(SingleFileScanningFrame, width = 50)
filePath.pack()
openFile = Button(SingleFileScanningFrame, text = lang_load.lang_OpenFile, command = openFileFunc, style = "Outline.TButton")
openFile.pack(side = "left", padx = 25)
checkFile = Button(SingleFileScanningFrame, text = lang_load.lang_CheckFile, command = checkFileFunc, style = "Outline.TButton")
checkFile.pack(side = "right", padx = 25)

Separator3 = Separator(root, orient = HORIZONTAL)
Separator3.pack(side = "bottom", padx = 10, pady = 3, fill = X)

# Clear Trash Loading
ClearTrashFrame = Frame(root)
ClearTrashFrame.pack(side = "bottom", pady = 10)
ProgressBar1 = Progressbar(ClearTrashFrame, orient = HORIZONTAL, length = 350, mode = 'indeterminate')
ProgressBar1.pack()
ClearTrash = Button(ClearTrashFrame, text = lang_load.lang_ClearTrash, command = ClearTrash, style = "Outline.TButton")
ClearTrash.pack(side = "bottom", padx = 25)

threading.Thread(target = icon.run, daemon = True).start()
root.config(menu = menubar)
on_exit()
root.mainloop()