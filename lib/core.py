import yara
import os

def CheckFile(filePath):
    filepath = {}
    path = os.path.abspath('.') + '/assets/rules/index.yar'
    rule = yara.compile(path)
    fp = open(filePath, 'rb')
    matches = rule.match(data = fp.read())
    fp.close()
    if len(matches) > 0:
        return True
    return False