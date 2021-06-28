import os
import re
from threading import Thread

urlRegEx = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
ipRegEx = "\\b(?!(?:10\.|127\.|172\.(?:1[6-9]|2[0-9]|3[0-2])\.|192\.168\.))((?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2(?:[0-4][0-9]|5[0-4])|[0-1]?[0-9]?[0-9])))\\b"

urlList = []
ipList = []

def extractUrls(file):
    urls = []
    results = re.findall(urlRegEx, file)
    if (len(results) != 0):
        for result in results:
            urlList.append(result[0] + "://" + result[1])
    return urlList


def extractIPs(file):
    ips = []
    results = re.findall(ipRegEx, file)
    if (len(results) != 0):
        for result in results:
            ipList.append(result)
    return ipList


def printList(list):
    counter = 0
    for item in list:
        counter += 1
        print("{}. {}".format(str(counter), item))


def printResult():
    global urlList, ipList
    urlList = list(set(urlList))
    ipList = list(set(ipList))

    print("\n---------------------URLs---------------------")
    if (urlList):
        print("List of URLs found in the application")
        printList(urlList)
    else:
        print("No URL was found")

    print("\n---------------------IP Addresses---------------------")
    if (ipList):
        print("List of IP addresses found in the application")
        printList(ipList)
    else:
        print("No IP address was found")

def startScan(folderPath):
    hasException = False
    for subdir, dirs, files in os.walk(folderPath):
        for file in files:
            try:
                fullpath = os.path.join(subdir, file)
                fileobj= open(fullpath, "r", errors = "ignore")
                filecontent = fileobj.read()
                fileobj.close()
            except Exception as e: 
                hasException = True

            try:
                thread1 = Thread(target = extractUrls, args = (filecontent, ))
                thread2 = Thread(target = extractIPs, args = (filecontent, ))

                thread1.start()
                thread2.start()

                thread1.join()
                thread2.join()
            except Exception as e:
                print("Error spawning threads")

    if hasException:
        print("Some results have have been ommitted due to exceptions")
    printResult()