import yara
import os

def CheckFile(filePath):
    filepath = {}
    rule = yara.compile(os.path.abspath('.') + '/lib/rules/index.yar')
    fp = open(filePath, 'rb')
    matches = rule.match(data = fp.read())
    fp.close()
    if len(matches) > 0:
        return True
    return False