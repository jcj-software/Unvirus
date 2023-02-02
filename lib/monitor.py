import glob
import getpass
from lib.core import *
from lib.lang import *
from tkinter.messagebox import *
import winreg

def getAllSub(path, dirlist = [], filelist = []):
    flist = os.listdir(path)
    for filename in flist:
        subpath = os.path.join(path, filename)
        if os.path.isdir(subpath):
            getAllSub(subpath, dirlist, filelist)
        if os.path.isfile(subpath):
            filelist.append(subpath)
    return dirlist, filelist


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "Desktop")[0]

def get_download():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    return winreg.QueryValueEx(key, "{374DE290-123F-4565-9164-39C4925E467B}")[0]

class monitor:
    stop = False
    username = getpass.getuser()
    download = get_download()
    desktop = get_desktop()
    black = []
    desktop_file = []
    download_file = []
    def __init__(self):
        try:
            with open('black.dat', 'rb') as f:
                self.black = pickle.load(f)
        except:
            self.black = []
    
    def monitor(self):
        while True:
            if self.stop == True:
                break
            test, self.desktop_file = getAllSub(self.desktop)
            test, self.download_file = getAllSub(self.download)
            for filename in self.desktop_file:
                if CheckFile(filename):
                    if filename not in self.black:
                        ask = askyesno('', filename + '\n' + lang_load.lang_FileStatus + lang_load.lang_Malicious + '\n' + lang_load.lang_Process)
                        if ask == False:
                            self.black.append(filename)
                            with open('black.dat', 'wb') as f:
                                pickle.dump(self.black, f)
                        elif ask == True:
                            os.remove(filename)
            for filename in self.download_file:
                if CheckFile(filename):
                    if filename not in self.black:
                        ask = askyesno('', filename + '\n' + lang_load.lang_FileStatus + lang_load.lang_Malicious + '\n' + lang_load.lang_Process)
                        if ask == False:
                            self.black.append(filename)
                            with open('black.dat', 'wb') as f:
                                pickle.dump(self.black, f)
                        elif ask == True:
                            os.remove(filename)