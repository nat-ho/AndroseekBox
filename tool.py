#!/usr/bin/env python3
import os
import sys
import subprocess
import ntpath
from modules.smsFraud import scan_sms_fraud
# from modules.spyware import scan_spyware
from libraries.xmlUtils import *
from libraries.apkutils import *


def print_usage():
    print("""---------------------USAGE---------------------
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
        reUnpack = input("Files already exist, do you wish to re unpack APK? (Y/N)")
        if (reUnpack.upper() == "Y"):
            subprocess.run("rm -r " + folderPath, shell=True)
        elif (reUnpack.upper() == "N"):
            return folderPath
        else:
            extract_files(userInput)
    
    print("APK given as input \nUnpacking now")
    jadx = os.getcwd() + "/dependencies/jadx-1.2.0/bin/jadx"
    # subprocess.run("mkdir -p " + folderPath, shell=True)
    subprocess.run(jadx + " -d {} {}".format(folderPath, apkLocation), shell=True)

    return folderPath


def get_xmlDoc(apkLocation):
    xmlDoc = parse_xml(get_folder_path(apkLocation) + "/resources/AndroidManifest.xml")
    return xmlDoc

    
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
    """.format(get_attribute(xmlDoc, "manifest", "package"), 
            get_attribute(xmlDoc, "manifest", "android:versionCode"),
            get_attribute(xmlDoc, "manifest", "android:versionName"),
            get_attribute(xmlDoc, "uses-sdk", "android:minSdkVersion"),
            get_attribute(xmlDoc, "uses-sdk", "android:targetSdkVersion"),
            get_attribute(xmlDoc, "application", "android:name"),
            get_attribute(xmlDoc, "application", "android:allowBackup"),
            get_attribute(xmlDoc, "application", "android:debuggable")))


def print_app_components(appComponents):
    print("---------------------Application Components---------------------")
    for appComponent in appComponents:
        if (appComponent):
            print(appComponent)


def print_module_selection():
    print("\n---------------------Module Selection---------------------")
    print("Enter number to execute a module. \nType 'exit' to quit the application.")
    
    print("""\n1. SMS Fraud""")


#Python 3.9 and below
def execute_module(userInput, folderPath, xmlDoc):
    switcher = {
        '1' : lambda : scan_sms_fraud(folderPath, xmlDoc),
        '2' : lambda : scan_spyware(folderPath, xmlDoc),
        'default' : lambda : print("\nUnrecognized module ID! Please enter again.")
    }
    return switcher.get(userInput, switcher.get('default'))()


#Python 3.10 and above
# def execute_module(userInput):
#     match userInput:
#         case '1':
#             scan_sms_fraud(folderPath, xmlDoc)
#         case '2':
#             scan_spyware(folderPath, xmlDoc)
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

except Exception as e:
    print(e)

print_module_selection()
userInput = input("\nModule: ")

while (userInput.lower() != "exit"):
    folderPath = get_folder_path(sys.argv[1])
    xmlDoc = get_xmlDoc(sys.argv[1])
    execute_module(userInput, folderPath, xmlDoc)

    print_module_selection()
    userInput = input("\nEnter another module: ")

print("\nGoodbye!")