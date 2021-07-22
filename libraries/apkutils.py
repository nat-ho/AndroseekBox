import os
import re
import colorama
from colorama import init, Fore, Style
from threading import Thread

urlRegEx = "(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+):?\d*)([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"
ipRegEx = '\"\\b(?!(?:10\.|127\.|172\.(?:1[6-9]|2[0-9]|3[0-2])\.|192\.168\.))((?:(?:2(?:[0-4][0-9]|5[0-5])|[0-1]?[0-9]?[0-9])\.){3}(?:(?:2(?:[0-4][0-9]|5[0-4])|[0-1]?[0-9]?[0-9])))\\b\"'
nativeLibraryLoadRegEx = "(System\.(loadLibrary|load)\(.*\))"
nativeMethodRegEx = "((private|public)\sstatic\snative.*\(.*\))"

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


def print_list(list, outputFile):
    counter = 0
    for item in list:
        counter += 1
        print("{}. {}".format(str(counter), item))
        outputFile.write("{}. {}\n".format(str(counter), item))


def print_result(outputFile):
    global urlList, ipList, nativeLibraryList, nativeMethodList
    urlList = list(set(urlList))
    ipList = list(set(ipList))
    nativeLibraryList = list(set(nativeLibraryList))
    nativeMethodList = list(set(nativeMethodList))

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------URLs---------------------\n")
    outputFile.write("\n---------------------URLs---------------------\n")
    if (urlList):
        print_list(urlList, outputFile)
    else:
        print(Fore.YELLOW + "No URL was found")
        outputFile.write("No URL was found")

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------IP Addresses---------------------\n")
    outputFile.write("\n---------------------IP Addresses---------------------\n")
    if (ipList):
        print_list(ipList, outputFile)
    else:
        print(Fore.YELLOW + "No IP address were found")
        outputFile.write("No IP address were found")
    
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Native Libraries Loaded---------------------\n")
    outputFile.write("\n---------------------Native Libraries Loaded---------------------\n")
    if (nativeLibraryList):
        print_list(nativeLibraryList, outputFile)
    else:
        print(Fore.YELLOW + "No native libraries were loaded")
        outputFile.write("No native libraries were loaded\n")
    
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Native Methods---------------------\n")
    outputFile.write("\n---------------------Native Methods---------------------\n")
    if (nativeMethodList):
        print_list(nativeMethodList, outputFile)
    else:
        print(Fore.YELLOW + "No native methods were found")
        outputFile.write("No native methods were found\n")


def start_initial_scan(folderPath, outputFile):
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
                print(Fore.RED + "Error spawning threads")

    if hasException:
        print(Fore.YELLOW + "Some results have have been ommitted due to exceptions")
    print_result(outputFile)