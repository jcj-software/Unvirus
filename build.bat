python -m pip install pyinstaller
pyinstaller --icon="assets/icon.ico" -w app.py --collect-all yara-python
pause