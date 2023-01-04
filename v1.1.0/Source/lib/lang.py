import pickle

class lang_load:
    def switchChinese(self):
        self.lang = "Chinese"
        self.lang_Malicious = "危险"
        self.lang_Undetected = "未发现危险"
        self.lang_OpenFile = "打开文件..."
        self.lang_CheckFile = "检查文件"
        self.lang_FileStatus = "文件状态："
        self.lang_Show = "显示主窗口"
        self.lang_Exit = "退出"
        self.lang_Process = "是否处理此文件？"
    
    def switchEnglish(self):
        self.lang = "English"
        self.lang_Malicious = "Malicious"
        self.lang_Undetected = "Undetected"
        self.lang_OpenFile = "Open File..."
        self.lang_CheckFile = "Check File"
        self.lang_FileStatus = "File Status: "
        self.lang_Show = "Show Main Window"
        self.lang_Exit = "Exit"
        self.lang_Process = "Whether to process this file?"
    
    def _switchEnglish(self):
        self.switchEnglish()
        with open('lang.dat', 'wb') as f:
            pickle.dump(self.lang, f)
        exit()
        
    def _switchChinese(self):
        self.switchChinese()
        with open('lang.dat', 'wb') as f:
            pickle.dump(self.lang, f)
        exit()
        
lang_load = lang_load()

try:
    with open('lang.dat', 'rb') as f:
        if pickle.load(f) == "Chinese":
            lang_load.switchChinese()
        elif pickle.load(f) == "English":
            lang_load.switchEnglish()
except:
    lang_load.switchEnglish()
