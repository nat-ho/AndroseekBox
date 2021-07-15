import javalang
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
        print("Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def find_imports(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.Import):
            if (node.path in importList):
                foundImportList.append((filePath, packageName, node.path, node.position.line, node.position.column))

    except Exception as e:
        print("Exception occured when parsing {} for imported classes : :{}".format(filePath, e))


def print_result():
    global foundApiList, foundImportList, foundPermissionList
    foundApiList = list(set(foundApiList))
    foundImportList = list(set(foundImportList))

    print("\n---------------------Related API Calls---------------------")
    if (foundApiList):
        print("\nList of API calls related to Click fraud found in the application:")

        for apiCallCount, apiCall in enumerate(foundApiList):
            print("{}.\tAPI Call: {}".format(apiCallCount+1, apiCall[2]))
            print("\tFile Path: {}".format(apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tLine Number & Column Number: ({}, {})".format(apiCall[3], apiCall[4]))
            print("-" * 60)
    else:
        print("No related API calls were found")

    print("\n---------------------Related Library Imports---------------------")
    if (foundImportList):
        print("\nList of class imports related to Click fraud found in the application:")

        for importCount, classImport in enumerate(foundImportList):
            print("{}.\tImport: {}".format(importCount+1, classImport[2]))
            print("\tFile Path: {}".format(classImport[0]))
            print("\tPackage: {}".format(classImport[1]))
            print("\tLine Number & Column Number: ({}, {})".format(classImport[3], classImport[4]))
            print("-" * 60)
    else:
        print("No related class imports were found")


def scan_click_fraud(folderPath, xmlDoc):
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
                print("Error spawing threads")

        except Exception as e:
            hasException = True
    
    if hasException:
        print("Some results have been ommitted due to exceptions")
    print_result()