import javalang
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


foundBackdoorApiList = []

# getRuntime: Returns runtime object that can be used to exectue arbitrary commands
runtimeApiCalls = {"getRuntime"}

# ProcessBuilder: Constructor for process builder objects that can be used to exectue arbitrary commands
processBuilderConstructor = {"ProcessBuilder"}

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

    except Exception as e:
        print("Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def print_result():
    global foundBackdoorApiList
    foundBackdoorApiList = list(set(foundBackdoorApiList))

    print("\n---------------------Related API Calls---------------------")
    if (foundBackdoorApiList):
        print("\nList of API calls related to backdoor found in the application:")

        for apiCallCount, apiCall in enumerate(foundBackdoorApiList):
            print("{}.\tAPI Call: {}".format(apiCallCount+1, apiCall[2]))
            print("\tFile Path: {}".format(apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
    else:
        print("No related API calls were found")


def scan_backdoor(folderPath, xmlDoc):
    hasException = False

    for filePath in Path(folderPath).rglob('*.java'):
        try:
            with open(filePath) as file:
                sourcecode = file.read()
                file.close()

            find_api_calls(filePath, sourcecode)

        except Exception as e:
            hasException = True
    
    if hasException:
        print("Some results have been ommitted due to exceptions")

    print_result()