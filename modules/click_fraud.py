import javalang
import colorama
from colorama import init, Fore, Style
from threading import Thread
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


foundImportList = []
foundApiList = []
foundPermissionList = []

# android.view.View and android.view.MotionEvent not included as it is used in most files
importList = {"android.webkit.WebView"}

# dispatchTouchEvent: Pass touch screen motion even down to target or this view
# setAlpha: Sets opacity of the view capable of making it completely transparent for click fraud
# performClick: Calls view OnClickListener
# obtain: Creates MotionEvent that can be used for auto clicking
# addJavascriptInterface: Injects suplied Java object into webview
# evaluateJavascript: Asynchronously evaluates JavaScript and returns result if available
# loadData: Loads given data into WebView
# loadDataWithBaseURL: Loads given data into WebView using baseUrl as the base URL for the content
# loadUrl: Loads given URL with optional HTTP headers
# setWebViewClient: Sets WebViewClient that will receive notifications and requests replacing current handler
# setWebChromeClient: Replaces current handler with chrome handler that can handle JavaScript dialogs, titles etc.
apiCallsList = {
    "dispatchTouchEvent", "performClick", "addJavascriptInterface", "evaluateJavascript", 
    "loadData", "loadDataWithBaseURL", "loadUrl", "setWebViewClient", "setWebChromeClient"
} # setAlpha() checked manually, obtain() not included as it is a common API call


def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member == "setAlpha" and node.arguments[0] == "1.0f"):
                foundApiList.append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in apiCallsList):
                foundApiList.append((filePath, packageName, node.member, node.position.line, node.position.column))

    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def find_imports(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.Import):
            if (node.path in importList):
                foundImportList.append((filePath, packageName, node.path, node.position.line, node.position.column))

    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing {} for imported classes : :{}".format(filePath, e))


def print_result(outputFile):
    global foundApiList, foundImportList, foundPermissionList
    foundApiList = list(set(foundApiList))
    foundImportList = list(set(foundImportList))

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Related API Calls---------------------")
    outputFile.write("\n[Click Fraud Module]\n")
    outputFile.write("\n---------------------Related API Calls---------------------\n")

    if (foundApiList):
        for apiCallCount, apiCall in enumerate(foundApiList):
            print("{}.\tAPI Call: {}".format(apiCallCount+1, apiCall[2]))
            print("\tFile Path: {}".format(apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
            outputFile.write("{}.\tAPI Call: {}\n".format(apiCallCount+1, apiCall[2]))
            outputFile.write("\tFile Path: {}\n".format(apiCall[0]))
            outputFile.write("\tPackage: {}\n".format(apiCall[1]))
            outputFile.write("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
    else:
        print(Fore.YELLOW + "No related API calls were found")
        outputFile.write("No related API calls were found\n")

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Related Library Imports---------------------")
    outputFile.write("\n---------------------Related Library Imports---------------------\n")

    if (foundImportList):
        for importCount, classImport in enumerate(foundImportList):
            print("{}.\tImport: {}".format(importCount+1, classImport[2]))
            print("\tFile Path: {}".format(classImport[0]))
            print("\tPackage: {}".format(classImport[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(classImport[3], classImport[4]))
            outputFile.write("{}.\tImport: {}\n".format(importCount+1, classImport[2]))
            outputFile.write("\tFile Path: {}\n".format(classImport[0]))
            outputFile.write("\tPackage: {}\n".format(classImport[1]))
            outputFile.write("\tLine Number & Column Number: ({}, {})\n".format(classImport[3], classImport[4]))
    else:
        print(Fore.YELLOW + "No related class imports were found")
        outputFile.write("No related class imports were found\n")


def scan_click_fraud(folderPath, xmlDoc, outputFile):
    hasException = False
    # find_permissions(xmlDoc)

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
                print(Fore.RED + "Error spawing threads")

        except Exception as e:
            hasException = True
    
    if hasException:
        print(Fore.YELLOW + "Some results have been ommitted due to exceptions")

    print_result(outputFile)