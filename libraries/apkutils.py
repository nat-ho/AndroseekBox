import os
import re
from threading import Thread

urlRegEx = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
ipRegEx = "\\b(?!(?:10\.|127\.|172\.(?:1[6-9]|2[0-9]|3[0-2])\.|192\.168\.))((?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2(?:[0-4][0-9]|5[0-4])|[0-1]?[0-9]?[0-9])))\\b"
nativeLibraryLoadRegEx = "(System\.(loadLibrary|load)\(.*\))"
nativeMethodRegEx = "(private|public)\sstatic\snative.*\(.*\)"

urlList = []
ipList = []
nativeLibraryList = []
nativeMethodList = []

def extract_nativeLibraryLoading(file):
    nativeLibrariesFound = re.findall(nativeLibraryLoadRegEx, file)
    if (len(nativeLibrariesFound) != 0): 
        for nativeLibrary in nativeLibrariesFound:
            nativeLibraryList.append(nativeLibrary[0])
    
    nativeMethodsFound = re.findall(nativeMethodRegEx, file)
    if (len(nativeMethodsFound) != 0):
        for nativeMethod in nativeMethodsFound:
            nativeMethodList.append(nativeMethod[0])


def extract_urls(file):
    urls = re.findall(urlRegEx, file)
    if (len(urls) != 0):
        for result in urls:
            urlList.append(result[0] + "://" + result[1])


def extract_ip(file):
    ips = re.findall(ipRegEx, file)
    if (len(ips) != 0):
        for result in ips:
            ipList.append(result)


def print_list(list):
    counter = 0
    for item in list:
        counter += 1
        print("{}. {}".format(str(counter), item))


def print_result():
    global urlList, ipList, nativeLibraryList, nativeMethodList
    urlList = list(set(urlList))
    ipList = list(set(ipList))
    nativeLibraryList = list(set(nativeLibraryList))
    nativeMethodList = list(set(nativeMethodList))

    print("\n---------------------URLs---------------------")
    if (urlList):
        print("List of URLs found in the application")
        print_list(urlList)
    else:
        print("No URL was found")

    print("\n---------------------IP Addresses---------------------")
    if (ipList):
        print("List of IP addresses found in the application")
        print_list(ipList)
    else:
        print("No IP address were found")
    
    print("\n---------------------Native Libraries Loaded---------------------")
    if (nativeLibraryList):
        print("List loaded native libraries found in the application")
        print_list(nativeLibraryList)
    else:
        print("No native libraries were loaded")
    
    print("\n---------------------Native Methods---------------------")
    if (nativeMethodList):
        print("List of native methods found in the application")
        print_list(nativeMethodList)
    else:
        print("No native methods were found")

def start_initial_scan(folderPath):
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
                thread1 = Thread(target = extract_urls, args = (filecontent, ))
                thread2 = Thread(target = extract_ip, args = (filecontent, ))
                thread3 = Thread(target = extract_nativeLibraryLoading, args = (filecontent, ))

                thread1.start()
                thread2.start()
                thread3.start()

                thread1.join()
                thread2.join()
                thread3.join()
            except Exception as e:
                print("Error spawning threads")

    if hasException:
        print("Some results have have been ommitted due to exceptions")
    print_result()