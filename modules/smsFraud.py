import os
import re
import javalang
from threading import Thread
from pathlib import Path


# apiRegexList = [".*sendMultimediaMessage\(.*", ".*sendMultipartTextMessage\(.*", ".*sendTextMessage\(.*", ".*sendTextMessageWithoutPersisting\(.*"]
apiCallsList = ["sendMultimediaMessage", "sendMultipartTextMessage", "sendTextMessage", "sendTextMessageWithoutPersisting"]
importRegexList = ["android.telephony.SmsManager", "android.telephony.SmsMessage"]
permissionRegexList = ["android\.permission\.READ_SMS", "android\.permission\.RECEIVE_SMS", "android\.permission\.SEND_SMS"]

foundApiList = []
foundXmlPermissionList = []
foundImportList = []

def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member in apiCallsList):
                foundApiList.append((filePath, packageName, node.member, node.position.line, node.position.column))

    except Exception as e:
        print("Exception occured when parsing {} : :{}".format(filePath, e))


def find_imports(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.Import):
            if (node.path in importRegexList):
                foundImportList.append((filePath, packageName, node.path, node.position.line, node.position.column))

    except Exception as e:
        print("Exception occured when parsing {} : :{}".format(filePath, e))


#Todo: Function to extract permissions from XML and possibly in classes
def find_permissions(folderPath):
    pass


#Todo: Function to print results
def print_result():
    global foundApiList, foundImportList
    print("\n---------------------Related API Calls---------------------")

    if (foundApiList):
        print("List of API calls related to SMS fraud found in the application")
        # print_list(urlList)

        for result in foundApiList:
            print("-" * 40)
            print("File Path: {}".format(result[0]))
            print("Package: {}".format(result[1]))
            print("API Call: {}".format(result[2]))
            print("Line Number & Column Number: ({}, {})".format(result[3], result[4]))

    else:
        print("No related API calls were found")

    print("\n---------------------Related Library Imports---------------------")

    if (foundImportList):
        print("List of library imports related to SMS fraud found in the application")

        for result in foundImportList:
            print("-" * 40)
            print("File Path: {}".format(result[0]))
            print("Package: {}".format(result[1]))
            print("Import: {}".format(result[2]))
            print("Line Number & Column Number: ({}, {})".format(result[3], result[4]))

    else:
        print("No related library imports were found")


def scan_sms_fraud(folderPath):
    hasException = False

    for filePath in Path(folderPath).rglob('*.java'):
        try:
            with open(filePath) as file:
                sourcecode = file.read()
                file.close()

            try:
                thread1 = Thread(target = find_api_calls, args = (filePath, sourcecode, ))
                thread2 = Thread(target = find_imports, args = (filePath, sourcecode, ))

                thread1.start()
                thread2.start()

                thread1.join()
                thread2.join()

            except Exception as e:
                print("Error spawing threads")

        except Exception as e:
            hasException = True
        
    find_permissions(folderPath)
    
    if hasException:
        print("Some results have been ommitted due to exceptions")
    print_result()