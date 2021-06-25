import os
import re

urlRegEx = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
ipRegEx = "\\b(?!(?:10\.|127\.|172\.(?:1[6-9]|2[0-9]|3[0-2])\.|192\.168\.))((?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2(?:[0-4][0-9]|5[0-4])|[0-1]?[0-9]?[0-9])))\\b"

urlList = []
ipList = []


def extractUrls(file):
    urls = []
    results = re.findall(urlRegEx, file)
    if (len(results) != 0):
        for component in results:
            urlList.append(component[0] + "://" + component[1])
    return urlList

def extractIPs(file):
    ips = []
    results = re.findall(ipRegEx, file)
    if (len(results) != 0):
        for component in results:
            ipList.append(component[0])
    return ipList

#Todo: extractGoogleAPIkeys

#Todo: printResults

#Main function
def startScan(folderPath):
    for subdir, dirs, files in os.walk(folderPath):
        for file in files:
            fullpath = os.path.join(subdir, file)
            fileobj= open(fullpath, "r", errors = "ignore")
            filecontent = fileobj.read()
            fileobj.close()

            #Call helper functions
            urlList = extractUrls(filecontent)
            ipList = extractIPs(filecontent)