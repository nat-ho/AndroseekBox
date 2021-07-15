import javalang
import colorama
from colorama import init, Fore, Style
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


foundBackdoorApiList = []
foundPermissionList = []

# getRuntime: Returns runtime object that can be used to exectue arbitrary commands
runtimeApiCalls = {"getRuntime"}

# ProcessBuilder: Constructor for process builder objects that can be used to exectue arbitrary commands
processBuilderConstructor = {"ProcessBuilder"}

# BIND_DEVICE_ADMIN: Required for DeviceAdminReceiver that can perform potentially dangerous device admin actions
# Meant to check for older versions of Android as deprecated starting with Android 9 (API level 28)
backdoorPermissionList = {"android.permission.BIND_DEVICE_ADMIN"}

# Binder: Android IPC mechanism that can be used for remote method invocation
# Requires manual verfication: 1)return null/zero   2)return Binder object
binderMethodDeclaration = {"onBind"}


def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member in runtimeApiCalls):
                foundBackdoorApiList.append((filePath, packageName, node.member, node.position.line, node.position.column))
        
        for path, node in tree.filter(javalang.tree.LocalVariableDeclaration):
            if (node.type.name in processBuilderConstructor):
                foundBackdoorApiList.append((filePath, packageName, node.type.name, node.position.line, node.position.column))
        
        for path, node in tree.filter(javalang.tree.MethodDeclaration):
            if (node.name in binderMethodDeclaration):
                foundBackdoorApiList.append((filePath, packageName, node.name, node.position.line, node.position.column))
        
    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def find_permissions(xmlDoc):
    try:
        tempPermissionList = get_attribute_list(xmlDoc, "uses-permission", "android:name")
        for permission in tempPermissionList:
            if (permission in backdoorPermissionList):
                foundPermissionList.append(permission)
    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing Android Manifest XML for permissions requested : :{}".format(e))


def print_result():
    global foundBackdoorApiList, foundPermissionList
    foundBackdoorApiList = list(set(foundBackdoorApiList))
    foundPermissionList = list(set(foundPermissionList))

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Related API Calls---------------------")
    if (foundBackdoorApiList):
        for apiCallCount, apiCall in enumerate(foundBackdoorApiList):
            print("{}.\tAPI Call: {}".format(apiCallCount+1, apiCall[2]))
            print("\tFile Path: {}".format(apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
    else:
        print(Fore.YELLOW + "No related API calls were found")

    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Related Permissions Declared---------------------")
    if (foundPermissionList):
        for permissionCount, permission in enumerate(foundPermissionList):
            print("{}.\t{}".format(permissionCount+1, permission))
    else:
        print(Fore.YELLOW + "No related permissions were found")


def scan_backdoor(folderPath, xmlDoc):
    hasException = False
    find_permissions(xmlDoc)

    for filePath in Path(folderPath).rglob('*.java'):
        try:
            with open(filePath) as file:
                sourcecode = file.read()
                file.close()

            find_api_calls(filePath, sourcecode)

        except Exception as e:
            hasException = True
    
    if hasException:
        print(Fore.YELLOW + "Some results have been ommitted due to exceptions")

    print_result()