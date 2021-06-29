import os
from re import U
import sys
import subprocess
import ntpath
from modules.smsFraud import *
from libraries.xmlUtils import *
from libraries.apkutils import *


def print_usage():
    print("""---------------------USAGE---------------------
    ./tool.py path_to_AndroidManifest.xml
    ./tool.py path_to_APKFile.APK
    """)

def extract_files(file):
    appName = ntpath.basename(file).split('.')[0]
    folderPath = "OutputAPKs/" + appName

    if (not os.path.isdir(folderPath)):
        #Todo: Add option to re-disassemble if files are already present

        print("APK given as input \nUnpacking now")

        jadx = os.getcwd() + "/dependencies/jadx-1.2.0/bin/jadx"
        # subprocess.run("mkdir -p " + folderPath, shell=True)
        subprocess.run(jadx + " -d {} {}".format(folderPath, file), shell=True)

        return folderPath
    
def print_app_details(xmlDoc):
    print("""\n---------------------Application Details---------------------
    Name            :{}
    Version Code    :{}
    Version Name    :{}
    Minimum SDK     :{}
    Target SDK      :{}
    App Name        :{}
    Allow Backup    :{}
    Debuggable      :{}
    """.format(get_attribute(xmlDoc, 'manifest', 'package'), 
            get_attribute(xmlDoc, 'manifest', 'android:versionCode'),
            get_attribute(xmlDoc, 'manifest', 'android:versionName'),
            get_attribute(xmlDoc, 'uses-sdk', 'android:minSdkVersion'),
            get_attribute(xmlDoc, 'uses-sdk', 'android:targetSdkVersion'),
            get_attribute(xmlDoc, 'application', 'android:name'),
            get_attribute(xmlDoc, 'application', 'android:allowBackup'),
            get_attribute(xmlDoc, 'application', 'android:debuggable')))

def print_exported_components(exportedComponents):
    print("---------------------Exported Components---------------------")
    for exportedComponent in exportedComponents:
        if (exportedComponent):
            print(exportedComponent)

def print_module_selection():
    print("\n---------------------Module Selection---------------------")
    print("Enter number to execute a module. \nType 'exit' to quit the application.")
    
    print("""\n1. SMS Fraud""")


#Python 3.9 and below
def execute_module(userInput):
    switcher = {
        '1' : lambda : scan_sms_fraud(outputPath),
        'default' : lambda : print("\nUnrecognized module ID! Please enter again.")
    }
    return switcher.get(userInput, switcher.get('default'))()

# #Python 3.10 and above
# def execute_module(userInput):
#     match userInput:
#         case '1':
#             scan_sms_fraud()
#         case _:
#             print("Unrecognized module ID!")


try:

    if (len(sys.argv[1:]) < 1):
        print_usage()
    
    else:
        inputExtension = sys.argv[1].split('.')[-1]
        appName = sys.argv[1].split('.')[0]
        
        if (inputExtension == 'xml'):
            xmlDoc = parse_xml(sys.argv[1])
            print_app_details(xmlDoc)
            print_exported_components(xmlDoc)

        elif (inputExtension == 'apk'):
            outputPath = extract_files(sys.argv[1])

            xmlDoc = parse_xml(outputPath + "/resources/AndroidManifest.xml")
            print_app_details(xmlDoc)

            exportedComponents = get_exported_components(xmlDoc)
            print_exported_components(exportedComponents)

            strings = parse_xml_strings(outputPath + "/resources/res/values/strings.xml")
            start_initial_scan(outputPath)

            deeplinks = get_deeplinks(xmlDoc)
            print_deepLinks_map(deeplinks)

        else:
            print_usage()

except Exception as e:
    print(e)


print_module_selection()
userInput = input("\nModule: ")

while (userInput.lower() != "exit"):
    execute_module(userInput)

    print_module_selection()
    userInput = input("\nEnter another module: ")

print("\nGoodbye!")