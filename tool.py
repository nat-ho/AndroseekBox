#!/usr/bin/env python3
import os
import sys
import subprocess
import ntpath
import colorama
from colorama import init, Fore, Style
from modules.sms_fraud import scan_sms_fraud
from modules.click_fraud import scan_click_fraud
from modules.spyware import scan_spyware
from modules.backdoor import scan_backdoor
from libraries.xmlUtils import *
from libraries.apkutils import *

colorama.init(autoreset=True)

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


def get_xmlDoc(apkLocation):
    xmlDoc = parse_xml(get_folder_path(apkLocation) + "/resources/AndroidManifest.xml")
    return xmlDoc

    
def print_app_details(xmlDoc):
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Application Details---------------------")
    print ("""
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
            get_attribute(xmlDoc, "application", "android:debuggable")))


def print_app_components(appComponents):
    print(Fore.CYAN + Style.BRIGHT + "---------------------Application Components---------------------\n")
    for appComponent in appComponents:
        if (appComponent):
            print(appComponent)


def print_module_selection():
    print(Fore.CYAN + Style.BRIGHT + "\n---------------------Module Selection---------------------\n")
    print("""Enter number to execute a module. \nType 'exit' to quit the application.
    1. SMS Fraud
    2. Click Fraud
    3. Spyware
    4. Backdoor""")
    

#Python 3.9 and below
def execute_module(userInput, folderPath, xmlDoc):
    switcher = {
        '1' : lambda : scan_sms_fraud(folderPath, xmlDoc),
        '2' : lambda : scan_click_fraud(folderPath, xmlDoc),
        '3' : lambda : scan_spyware(folderPath, xmlDoc),
        '4' : lambda : scan_backdoor(folderPath, xmlDoc),
        'default' : lambda : print(Fore.RED + "\nUnrecognized module ID! Please enter again.")
    }
    return switcher.get(userInput, switcher.get('default'))()


# #Python 3.10 and above
# def execute_module(userInput):
#     match userInput:
#         case '1':
#             scan_sms_fraud(folderPath, xmlDoc)
#         case '2':
#             scan_click_fraud(folderPath, xmlDoc)
#         case '3':
#             scan_spyware(folderPath, xmlDoc)
#         case '4':
#             scan_backdoor(folderPath, xmlDoc)
#         case _:
#             print(Fore.RED + "Unrecognized module ID!")


try:

    if (len(sys.argv[1:]) < 1):
        print_usage()
        sys.exit(Fore.RED + "Please run the program again with the required files!")
    
    else:
        inputExtension = sys.argv[1].split('.')[-1]
        appName = sys.argv[1].split('.')[0]
        
        if (inputExtension == 'xml'):
            xmlDoc = parse_xml(sys.argv[1])
            print_app_details(xmlDoc)
            print_app_components(xmlDoc)

        elif (inputExtension == 'apk'):
            outputPath = extract_files(sys.argv[1])

            xmlDoc = parse_xml(outputPath + "/resources/AndroidManifest.xml")
            print_app_details(xmlDoc)

            appComponents = get_app_components(xmlDoc)
            print_app_components(appComponents)

            strings = parse_xml_strings(outputPath + "/resources/res/values/strings.xml")
            start_initial_scan(outputPath)

            deeplinks = get_deeplinks(xmlDoc)
            print_deepLinks_map(deeplinks)

        else:
            print_usage()
            sys.exit(Fore.RED + "Please run the program again with the required files!")

except Exception as e:
    print(Fore.RED + e)

print_module_selection()
userInput = input("\nModule: ")

while (userInput.lower() != "exit"):
    folderPath = get_folder_path(sys.argv[1])
    xmlDoc = get_xmlDoc(sys.argv[1])
    execute_module(userInput, folderPath, xmlDoc)

    print_module_selection()
    userInput = input("\nEnter another module: ")

print(Fore.CYAN + "\nGoodbye!")