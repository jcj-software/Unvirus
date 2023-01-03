from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
from lib.core import *
from lib.lang import *

root = Tk()
root.title("Unvirus-1")
root.geometry("400x300")
root.iconbitmap('assets/icon.ico')

def openFileFunc():
    filePath.delete(0, END)
    filePath.insert(0, askopenfilename())
    
def checkFileFunc():
    if CheckFile(filePath.get()) == True:
        fileStatusFrame.pack(side = "top")
        fileStatusUndetectedText.set("")
        fileStatusMaliciousText.set(lang_load.lang_Malicious)
    else:
        fileStatusFrame.pack(side = "top")
        fileStatusMaliciousText.set("")
        fileStatusUndetectedText.set(lang_load.lang_Undetected)
def aboutFunc():
    showinfo("关于Unvirus安全软件", """
关于Unvirus安全软件
Unvirus的历史：
    Unvirus —— 2023年1月1日由Jiang ChengJun先生开始开发；
    lib.core核心支持库 —— 2023年1月2日由Jiang ChengJun先生开发完毕；
    在Jiang ChengJun先生坚持使用免费原则的情况下，
    Unvirus-1.0.0 —— 2023年1月3日由Jiang ChengJun先生开发完毕；
    Unvirus-1.0.0 —— 2023年1月3日由Jiang ChengJun先生在Github上发布；
    Unvirus-1.1.0 —— 将会在2023年1月4日由Jiang ChengJun先生开始开发，
    预计2023年1月11日发布。
    
版权所有 © 2023 Jiang Chengjun
""")
# Menubar Loading
menubar = Menu(root)
Language = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = '语言(Language)', menu = Language)
Language.add_command(label = 'English', command = lang_load._switchEnglish)
Language.add_command(label = '中文', command = lang_load._switchChinese)

# Buttons Loading
about = Button(root, text = "关于Unvirus安全软件", command = aboutFunc)
about.pack(side = "bottom")
ButtonFrame = Frame(root)
ButtonFrame.pack(side = "bottom")
openFile = Button(ButtonFrame, text = lang_load.lang_OpenFile, command = openFileFunc)
openFile.pack(side = "left")
checkFile = Button(ButtonFrame, text = lang_load.lang_CheckFile, command = checkFileFunc)
checkFile.pack(side = "right")

# File Path Loading
filePathFrame = Frame(root)
filePathFrame.pack(side = "bottom")
filePath = Entry(filePathFrame, width = 50)
filePath.pack(side = "top")

# File Status Loading
fileStatusFrame = Frame(root)
fileStatusLabel = Label(fileStatusFrame, text = lang_load.lang_FileStatus)
fileStatusLabel.pack(side = "left")
fileStatusMaliciousText = StringVar()
fileStatusMalicious = Label(fileStatusFrame, textvariable = fileStatusMaliciousText, fg = "red")
fileStatusMalicious.pack(side = "left")
fileStatusUndetectedText = StringVar()
fileStatusUndetected = Label(fileStatusFrame, textvariable = fileStatusUndetectedText, fg = "green")
fileStatusUndetected.pack(side = "left")


root.config(menu = menubar)
root.mainloop()