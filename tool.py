import os
import sys
import subprocess
import ntpath
from libraries.xmlUtilities import *


def print_usage():
    print("""---------------------USAGE---------------------
    ./tool.py path_to_AndroidManifest.xml
    ./tool.py path_to_APKFile.APK
    """)

def extract_files(file):
    appName = ntpath.basename(file).split('.')[0]
    folderPath = "APKs/" + appName

    if not os.path.isdir(folderPath):
        #subprocess.run("mkdir -p " + folderPath, shell=True)
        subprocess.run('java -jar '+ os.getcwd()+"/dependencies/apktool.jar" +' d {} -o {}'.format(file,folderPath), shell=True)
    

def print_app_details(xmlDoc):
    print("""---------------------Application Details---------------------
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

def print_exported_components(xmlDoc):
    print("---------------------Exported Components---------------------")
    exportedComponents = get_exported_components(xmlDoc)
    for exportedComponent in exportedComponents:
        if (exportedComponent):
            print(exportedComponent)


try:

    if len(sys.argv[1:]) < 1:
        print_usage()
    
    else:
        inputExtension = sys.argv[1].split('.')[-1]
        
        if inputExtension == 'xml':
            xmlDoc = parse_xml(sys.argv[1])
            print_app_details(xmlDoc)
            print_exported_components(xmlDoc)

        elif inputExtension == 'apk':
            extract_files(sys.argv[1])
            pass

        else:
            print_usage()

except Exception as e:
    print(e)

