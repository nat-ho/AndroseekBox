#!/usr/bin/env python3
import os
import sys
import subprocess
import ntpath
import shutil
import colorama
from colorama import init, Fore, Style
from modules.sms_fraud import scan_sms_fraud
from modules.click_fraud import scan_click_fraud
from modules.spyware import print_permissions, scan_spyware
from modules.backdoor import scan_backdoor
from libraries.xmlUtils import *
from libraries.apkUtils import *

colorama.init(autoreset=True)
outputFile = None
outputFile = None
appName = None

def print_usage():
    print(Fore.YELLOW + """---------------------USAGE---------------------
    ./tool.py path_to_AndroidManifest.xml
    ./tool.py path_to_APKFile.APK
    """)


def get_folder_path(apkLocation):
    appName = ntpath.basename(apkLocation).split('.')[0]
    return "OutputAPKs/" + appName


def extract_files(apkLocation):
    folderPath = get_folder_path(apkLocation)

    # If files exist, provide user to continue or re unpack APK
    if (os.path.isdir(folderPath)):
        reUnpack = input(Fore.YELLOW + "Files already exist, do you wish to re unpack APK? (Y/N)")
        if (reUnpack.upper() == "Y"):
            subprocess.run("rm -r " + folderPath, shell=True)
        elif (reUnpack.upper() == "N"):
            return folderPath
        else:
            extract_files(userInput)
    
    print(Fore.GREEN + Style.BRIGHT + "APK given as input \nUnpacking now")
    jadx = os.getcwd() + "/dependencies/jadx-1.2.0/bin/jadx"
    # subprocess.run("mkdir -p " + folderPath, shell=True)
    subprocess.run(jadx + " -d {} {}".format(folderPath, apkLocation), shell=True)

    return folderPath

def moveZipToOutput(zipLocation):
    newZipPath = "OutputAPKs/" + zipLocation
    shutil.move(zipLocation, newZipPath)
    return newZipPath


def create_output_file(outputApkPath, appName):
    outputFileName = appName + "_output.txt"
    outputFilePath = outputApkPath + "/" + outputFileName

    text_file = open(outputFilePath, "w+")
    return text_file


def get_output_file(outputApkPath, appName):
    outputFileName = appName + "_output.txt"
    outputFilePath = outputApkPath + "/" + outputFileName

    text_file = open(outputFilePath, "a")
    return text_file
    

def get_xmlDoc(apkLocation):
    xmlDoc = parse_xml(get_folder_path(apkLocation) + "/resources/AndroidManifest.xml")
    return xmlDoc

    
def print_app_details(xmlDoc, outputFile):
    appDetailsHeader = "\n---------------------Application Details---------------------"
    print(Fore.CYAN + Style.BRIGHT + appDetailsHeader)
    outputFile.write(appDetailsHeader)

    addDetailsBody = """
    Name            :{}
    Version Code    :{}
    Version Name    :{}
    Minimum SDK     :{}
    Target SDK      :{}
    App Name        :{}
    Allow Backup    :{}
    Debuggable      :{}
    """.format(get_attribute(xmlDoc, "manifest", "package"), 
            get_attribute(xmlDoc, "manifest", "android:versionCode"),
            get_attribute(xmlDoc, "manifest", "android:versionName"),
            get_attribute(xmlDoc, "uses-sdk", "android:minSdkVersion"),
            get_attribute(xmlDoc, "uses-sdk", "android:targetSdkVersion"),
            get_attribute(xmlDoc, "application", "android:name"),
            get_attribute(xmlDoc, "application", "android:allowBackup"),
            get_attribute(xmlDoc, "application", "android:debuggable"))
    print (addDetailsBody)
    outputFile.write(addDetailsBody)


def print_app_components(appComponents, outputFile):
    print(Fore.CYAN + Style.BRIGHT + "---------------------Application Components---------------------\n")
    outputFile.write("\n---------------------Application Components---------------------\n")

    for appComponent in appComponents:
        if (appComponent[1] == "Exported"):
            print("{} {}".format(appComponent[0], Fore.YELLOW + Style.BRIGHT + "(Exported)"))
            outputFile.write("{} {}\n".format(appComponent[0], "(Exported)"))
        else:
            print(appComponent[0])
            outputFile.write(appComponent[0] + "\n")

def print_app_permissions(appPermissions, outputFile):
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Application Permissions---------------------\n")
    outputFile.write("\n---------------------Application Permissions---------------------\n")

    for appPermission in appPermissions:
        print(appPermission)
        outputFile.write(appPermission + "\n")


def print_app_strings(appStrings, outputFile):
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Application Strings---------------------\n")
    outputFile.write("\n---------------------Application Strings---------------------\n")

    for appString in appStrings:
        print(appString)
        outputFile.write(appString + "\n")

def print_module_selection():
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Module Selection---------------------\n")
    print("""Enter number to execute a module. \nType 'exit' to quit the application.
    1. SMS Fraud
    2. Click Fraud
    3. Spyware
    4. Backdoor""")
    

# Python 3.9 and below
def execute_module(userInput, folderPath, xmlDoc, outputFile):
    switcher = {
        '1' : lambda : scan_sms_fraud(folderPath, xmlDoc, outputFile),
        '2' : lambda : scan_click_fraud(folderPath, xmlDoc, outputFile),
        '3' : lambda : scan_spyware(folderPath, xmlDoc, outputFile),
        '4' : lambda : scan_backdoor(folderPath, xmlDoc, outputFile),
        'default' : lambda : print(Fore.RED + "\nUnrecognized module ID! Please enter again.")
    }
    return switcher.get(userInput, switcher.get('default'))()


# Python 3.10 and above
# def execute_module(userInput):
#     match userInput:
#         case '1':
#             scan_sms_fraud(folderPath, xmlDoc, outputFile)
#         case '2':
#             scan_click_fraud(folderPath, xmlDoc, outputFile)
#         case '3':
#             scan_spyware(folderPath, xmlDoc, outputFile)
#         case '4':
#             scan_backdoor(folderPath, xmlDoc, outputFile)
#         case _:
#             print(Fore.RED + "Unrecognized module ID!")

apkOrZip = False

try:

    if (len(sys.argv[1:]) < 1):
        print_usage()
        sys.exit(Fore.RED + "Please run the program again with the required files!")
    
    else:
        inputExtension = sys.argv[1].split('.')[-1]
        appName = sys.argv[1].split('.')[0]
        
        if (inputExtension == 'xml'):
            print("XML file given as input. File be parsed as AndroidManifest")

            xmlDoc = parse_xml(sys.argv[1])
            print_app_details(xmlDoc)

            appComponents = get_app_components(xmlDoc)
            print_app_components(appComponents)

        elif (inputExtension == 'apk' or os.path.isdir(sys.argv[1])):
            if (inputExtension == 'apk'):
                outputPath = extract_files(sys.argv[1])
            else:
                outputPath = moveZipToOutput(sys.argv[1])

            apkOrZip = True
            outputFile = create_output_file(outputPath, appName)

            xmlDoc = parse_xml(outputPath + "/resources/AndroidManifest.xml")
            print_app_details(xmlDoc, outputFile)

            appComponents = get_app_components(xmlDoc)
            print_app_components(appComponents, outputFile)

            appPermissions = get_app_permissions(xmlDoc)
            print_app_permissions(appPermissions, outputFile)

            strings = parse_xml_strings(outputPath + "/resources/res/values/strings.xml")
            # print_app_strings(strings, outputFile)

            start_initial_scan(outputPath, outputFile)

            deeplinks = get_deeplinks(xmlDoc)
            print_deepLinks_map(deeplinks, outputFile)
            outputFile.close()
        
        else:
            print_usage()
            sys.exit(Fore.RED + "Please run the program again with the required files!")

except Exception as e:
    print(e)

if (apkOrZip == True):
    print_module_selection()
    userInput = input("\nModule: ")

    while (userInput.lower() != "exit"):
        outputFile = get_output_file(outputPath, appName)

        folderPath = get_folder_path(sys.argv[1])
        xmlDoc = get_xmlDoc(sys.argv[1])
        execute_module(userInput, folderPath, xmlDoc, outputFile)

        print_module_selection()
        outputFile.close()
        userInput = input("\nEnter another module: ")

    print(Fore.CYAN + "\nGoodbye!")