import pickle
import win32api
import win32con
import sys

try:
    with open('setting.dat', 'rb') as f:
        setting = pickle.load(f)
except:
    setting = {'monitor': True, 'startup': True}

key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, 'Software\Microsoft\Windows\CurrentVersion\Run', 0, win32con.KEY_ALL_ACCESS)

if setting['startup'] == True:
    win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, sys.argv[0])
    win32api.RegCloseKey(key)
elif setting['startup'] == False:
    win32api.RegSetValueEx(key, "Unvirus", 0, win32con.REG_SZ, "")
    win32api.RegCloseKey(key)