import hashlib
import requests
from lxml import html

def CalcHash(filePath):
    with open(filePath,'rb') as f:
        obj = hashlib.sha256()
        obj.update(f.read())
        result = obj.hexdigest()
        return result
         
def CheckFile(filePath):
    url = "https://www.virustotal.com/old-browsers/file/" + str(CalcHash(filePath))
    try:
        page = requests.get(url, headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; InfoPath.3; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0)"})
    except:
        page = requests.get(url, headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; InfoPath.3; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Tablet PC 2.0)"})
    tree = html.fromstring(page.text) 
    text = tree.xpath('//*[@id="detections"]/text()')
    try:
        num = int(text[0].split("/")[0][9:])
        result = (num != 0)
        return result
    except:
        return False
