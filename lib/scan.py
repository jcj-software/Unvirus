import glob
import getpass
from lib.core import *
from lib.lang import *
from tkinter.messagebox import *

class scan:
    stop = False
    username = getpass.getuser()
    black = []
    file = []
    def __init__(self):
        try:
            with open('black.dat', 'rb') as f:
                self.black = pickle.load(f)
        except:
            self.black = []
    
    def scan(self, func):
        self.file = []
        for filename in glob.glob(r'C:/*.exe'):
            self.file.append(filename)
            if self.stop:
                break
        for filename in glob.glob(r'C:/*/*.exe'):
            self.file.append(filename)
            if self.stop:
                break
        for filename in glob.glob(r'C:/*/*/*.exe'):
            self.file.append(filename)
            if self.stop:
                break
        for filename in self.file:
            if self.stop:
                break
            try:
                if CheckFile(filename):
                    if filename not in self.black:
                        ask = askyesno('', filename + '\n' + lang_load.lang_FileStatus + lang_load.lang_Malicious + '\n' + lang_load.lang_Process)
                        if ask == False:
                            self.black.append(filename)
                            with open('black.dat', 'wb') as f:
                                pickle.dump(self.black, f)
                        elif ask == True:
                            os.remove(filename)
            except:
                continue
        func()
        showinfo('Unvirus', lang_load.lang_Scanned)