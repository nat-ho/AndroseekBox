import javalang
import re
import colorama
from colorama import init, Fore, Style
from threading import Thread
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


extractedScreenCaptureInfo = [[] for i in range(3)]
extractedDeviceReconInfo = [[] for i in range(3)]
extractedSLocationTrackingInfo = [[] for i in range(3)]
# extractedKeyloggerInfo = [[] for i in range(3)]
# extractedCameraRecordingInfo = [[] for i in range(3)]
# extractedClipboardTrackingInfo = [[] for i in range(3)]

# SCREEN CAPTURE
# createScreenCaptureIntent: Creates an intent in order to start screen capture
# getMediaProjection: Retrieves MediaProjection obtained from successful capture request
screenCaptureImports = {
    "android.media.projection.MediaProjectionManager"
}
screenCaptureAPIs = {
    "createScreenCaptureIntent", "getMediaProjection"
}
screenCapturePermissions = {
    "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"
}

# DEVICE RECON
# getLine1Number: Retrieve phone number of SIM card
# getSimOperator: Retrieve mobile country code and mobile network code of SIM provider
# loadClass("android.os.SystemProperties"): android.os.SystemProperties is a hidden class so this check determines if reflection was used to gain access and information about system properties
deviceReconImports = {
    "android.telephony.TelephonyManager"
}
deviceReconAPIs = {
    "getLine1Number", "getSimOperator", "loadClass"  #Check if loading android.os.SystemProperties
}
deviceReconPermissions = {
    "android.permission.READ_PHONE_STATE", "android.permission.READ_SMS", "android.permission.READ_PHONE_NUMBERS"
}

# LOCATION TRACKING
# getLastKnownLocation: Uses LocationManager to get last known location from device's provider
# getLastLocation: Recommended method to get last known location by using Google Play services location API - fused location provider (https://developer.android.com/training/location/retrieve-current & https://blog.teamtreehouse.com/beginners-guide-location-android)
# onLocationChanged: Called when location of device has changed
# onProviderDisabled: Called by LocationListener when provider its registered with becomes disabled
# onStatusChanged: Called by LocationListener when provider its registered with has a status change (Out of service, temporarily unavailable, availble) - Deprecated in API level 29 and will not be invoked on Android Q and above
# getLatitude & getLongitude: Uses locationManager to retrive latitude and longtitude of device location
# getCallState: Retrieve state of all calls on device (Calls in Telephony stack and other calls via other ConnectionService implementations) - Deprecated in API level S
# getCallStateForSubscription: Retrieve call state for a specific telephony subscription (idle, ringing or offhook)
# isInCall: Determine if there is an ongoing phone call originating from either a manager or self-managed ConnectionService (dialing, ringing, active or holding states)
# getDeviceId & getImei: Will be used to check for devices running below Android 10 as SecurityException occurs for apps targeting Android 10 and above (https://developer.android.com/about/versions/10/privacy/changes#data-ids)
# loadClass("android.os.SystemProperties"): android.os.SystemProperties is a hidden class so this check determines if reflection was used to gain access and information about system properties
locationTrackingImports = {
    "android.location.LocationManager", "android.location.LocationListener", "android.location.Location", 
    "com.google.android.gms.common.ConnectionResult", "com.google.android.gms.common.api.GoogleApiClient", 
    "com.google.android.gms.location.LocationListener", "com.google.android.gms.location.LocationRequest", 
    "com.google.android.gms.location.LocationServices", "android.telephony.TelephonyManager"
}
locationTrackingAPIs = {
    "getLastKnownLocation", "getLastLocation", "onLocationChanged", "onProviderDisabled", "onStatusChanged", 
    "getLatitude", "getLongitude", "getCallState", "getCallStateForSubscription", "isInCall",  "getDeviceId", "getImei", 
    "loadClass" #Check if loading android.os.SystemProperties
} 
locationTrackingPermissions = {
    "android.permission.ACCESS_COARSE_LOCATION", "android.permission.ACCESS_FINE_LOCATION", 
    "android.permission.ACCESS_BACKGROUND_LOCATION", "android.permission.READ_PHONE_STATE"
}

""" (Not in current use as these checks may return a lot of false positive results due to the library and API calls being very common even in benign apps)
# KEYLOGGER
# getText: Detects if Accessibility Service is used in conjunction with getText() method which can be used to log keystrokes to the console
# https://github.com/n37sn4k3/Android-Accessibility-Keylogger
# https://github.com/bshu2/Android-Keylogger
keyloggerImports = {
    "android.view.accessibility.AccessibilityNodeInfo", "android.view.accessibility.AccessibilityEvent"
}
keyloggerAPIs = {
    "getText", "getEventType", "getAction"
}
keyloggerPermissions = {
    "android.permission.BIND_ACCESSIBILITY_SERVICE"
}

# CAMERA RECORDING MONITORS
# setAudioSource & setVideoSource: Sets video and audio source used for recording
# setOutputFile: Sets file object to be written during recording
# prepare & start: Controls capturing and encoding of data
# getSurface: Retrieves surface object from MediaRecorder
# read: Audio data is being read
# getActiveMicrophones: Retrieve active microphones
# getAudioSource: Returns the audio recording source
# startRecording & stop: Start/stop device audio recording from the AudioRecord instance
cameraRecordingImports = {
    "android.media.MediaRecorder", "android.media.AudioRecord"
}
cameraRecordingAPIs = {
    "setAudioSource", "setVideoSource", "setOutputFile", "prepare", "getSurface", "read", 
    "getActiveMicrophones", "getAudioSource", "startRecording"
}
cameraRecordingPermissions = {
    "android.permission.CAMERA", "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.RECORD_AUDIO"
}

# CLIPBOARD TRACKING - No permission required to register a listener that can transmit device's clipboard to a remote server
# hasPrimaryClip: App is checking if clipboard contains data
# getPrimaryClip: App is retrieving text from the clipboard
# hasText: Deprecated method since API level 11 for hasPrimaryClip()
# getText: Deprecated method since API level 11 for getPrimaryClip()
clipboardTrackingImports = {
    "android.content.ClipboardManager"
}
clipboardTrackingAPIs = {
    "hasPrimaryClip", "getPrimaryClip", "hasText", "getText"
}
"""


def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member in screenCaptureAPIs):
                extractedScreenCaptureInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            if (node.member in deviceReconAPIs):
                extractedDeviceReconInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            if (node.member in locationTrackingAPIs):
                extractedSLocationTrackingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            # if (node.member in keyloggerAPIs):
            #     extractedKeyloggerInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            # if (node.member in cameraRecordingAPIs):
            #     extractedCameraRecordingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            # if (node.member in clipboardTrackingAPIs):
            #     extractedClipboardTrackingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def find_imports(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.Import):
            if (node.path in screenCaptureImports):
                extractedScreenCaptureInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in deviceReconImports):
                extractedDeviceReconInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in locationTrackingImports):
                extractedSLocationTrackingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            # elif (node.path in keyloggerImports):
            #     extractedKeyloggerInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            # elif (node.path in cameraRecordingImports):
            #     extractedCameraRecordingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            # elif (node.path in clipboardTrackingImports):
            #     extractedClipboardTrackingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))

    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing {} for imported classes : :{}".format(filePath, e))


def find_permissions(xmlDoc):
    try:
        tempPermissionList = get_attribute_list(xmlDoc, "uses-permission", "android:name")

        for permission in tempPermissionList:
            if (permission in screenCapturePermissions):
                extractedScreenCaptureInfo[2].append(permission)
            elif (permission in deviceReconPermissions):
                extractedDeviceReconInfo[2].append(permission)
            elif (permission in locationTrackingPermissions):
                extractedSLocationTrackingInfo[2].append(permission)
            # elif (permission in keyloggerPermissions):
            #     extractedKeyloggerInfo[2].append(permission)
            # elif (permission in cameraRecordingPermissions):
            #     extractedCameraRecordingInfo[2].append(permission)

    except Exception as e:
        print(Fore.YELLOW + "Exception occured when parsing Android Manifest XML for permissions requested : :{}".format(e))


# Print runner function
def print_result(outputFile):
    global extractedScreenCaptureInfo, extractedDeviceReconInfo, extractedKeyloggerInfo, extractedSLocationTrackingInfo, extractedCameraRecordingInfo, extractedClipboardTrackingInfo

    print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to screen capture Spyware" + "-" * 40)
    outputFile.write("\n[Spyware Module]\n")
    outputFile.write("\n" + "-" * 40 + "Information related to screen capture Spyware" + "-" * 40 + "\n")
    if (extractedScreenCaptureInfo):
        print_all_information(extractedScreenCaptureInfo, outputFile)

    print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to device recon Spyware" + "-" * 40)
    outputFile.write("\n" + "-" * 40 + "Information related to device recon Spyware" + "-" * 40 + "\n")
    if (extractedDeviceReconInfo):
        print_all_information(extractedDeviceReconInfo, outputFile)
    
    print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to location tracking Spyware" + "-" * 40)
    outputFile.write("\n" + "-" * 40 + "Information related to location tracking Spyware" + "-" * 40 + "\n")
    if (extractedSLocationTrackingInfo):
        print_all_information(extractedSLocationTrackingInfo, outputFile)

    # print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to keylogger Spyware" + "-" * 40)
    # outputFile.write("\n" + "-" * 40 + "Information related to keylogger Spyware" + "-" * 40 + "\n")
    # if (extractedKeyloggerInfo):
    #     print_all_information(extractedKeyloggerInfo, outputFile)

    # print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to camera recording Spyware" + "-" * 40)
    # outputFile.write("\n" + "-" * 40 + "Information related to camera recording Spyware" + "-" * 40 + "\n")
    # if (extractedCameraRecordingInfo):
    #     print_all_information(extractedCameraRecordingInfo, outputFile)

    # print(Fore.CYAN + Style.BRIGHT + "-" * 40 + "Information related to clipboard tracking Spyware" + "-" * 40)
    # outputFile.write("\n" + "-" * 40 + "Information related to clipboard tracking Spyware" + "-" * 40 + "\n")
    # if (extractedClipboardTrackingInfo):
    #     print_all_information(extractedClipboardTrackingInfo, outputFile)
   

def print_all_information(extractedInfo, outputFile):
    for category, infoList in enumerate(extractedInfo):
        filteredInfo = list(set(infoList))
        if category == 0:
            print(Fore.GREEN + "[Related API Calls]")
            outputFile.write("[Related API Calls]\n")
            print_apiCalls(filteredInfo, outputFile)
        elif category == 1:
            print(Fore.GREEN + "[Related Class Imports]")
            outputFile.write("[Related Class Imports]\n")
            print_classImports(filteredInfo, outputFile)
        elif category == 2:
            print(Fore.GREEN + "[Related Permissions]")
            outputFile.write("[Related Permissions]\n")
            print_permissions(filteredInfo, outputFile)


def print_apiCalls(apiCalls, outputFile):
    if apiCalls:
        for apiCallCount, apiCall in enumerate(apiCalls):
            print("{}.\tAPI Call: {}".format(apiCallCount+1,apiCall[2]))
            print("\tFile Path: {}".format(apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
            outputFile.write("{}.\tAPI Call: {}\n".format(apiCallCount+1,apiCall[2]))
            outputFile.write("\tFile Path: {}\n".format(apiCall[0]))
            outputFile.write("\tPackage: {}\n".format(apiCall[1]))
            outputFile.write("\tLine Number & Column Number: ({}, {})\n".format(apiCall[3], apiCall[4]))
    else:
        print(Fore.YELLOW + "No related API Calls were found\n")
        outputFile.write("No related API Calls were found\n")


def print_classImports(classImports, outputFile):
    if classImports:
        for importCount, classImport in enumerate(classImports):
            print("{}.\tImport: {}".format(importCount+1, classImport[2]))
            print("\tFile Path: {}".format(classImport[0]))
            print("\tPackage: {}".format(classImport[1]))
            print("\tLine Number & Column Number: ({}, {})\n".format(classImport[3], classImport[4]))
            outputFile.write("{}.\tImport: {}\n".format(importCount+1, classImport[2]))
            outputFile.write("\tFile Path: {}\n".format(classImport[0]))
            outputFile.write("\tPackage: {}\n".format(classImport[1]))
            outputFile.write("\tLine Number & Column Number: ({}, {})\n".format(classImport[3], classImport[4]))
    else:
        print(Fore.YELLOW + "No related Class Imports were found\n")
        outputFile.write("No related Class Imports were found\n")


def print_permissions(permissions, outputFile):
    if permissions:
        for permissionCount, permission in enumerate(permissions):
            print("{}.\t{}\n".format(permissionCount+1, permission))
            outputFile.write("{}.\t{}\n".format(permissionCount+1, permission))
    else:
        print(Fore.YELLOW + "No related Permissions were found\n")
        outputFile.write("No related Permissions were found\n")
    print("\n")


""" (Data cleaning functions to remove some false positive results)
def cleanup_keylogger_accessibilityEvent_apiCalls(apiCall):
    if (apiCall == "getEventType" or apiCall == "getAction"):
        return False
    return apiCall


def cleanup_keylogger_accessibilityNodeInfo_apiCalls(apiCall):
    if (apiCall == "getText"):
        return False
    return apiCall


def cleanup_keylogger_imports(importClass):
    if (importClass == "android.view.accessibility.AccessibilityNodeInfo" or 
            importClass == "android.view.accessibility.AccessibilityEvent"):
        return False
    return importClass


def cleanup_camRecord_apiCalls(apiCall):
    if (apiCall == "setAudioSource" or apiCall == "setVideoSource" or apiCall == "setOutputFile" or apiCall == "prepare" 
            or apiCall == "start" or apiCall == "getSurface"):
        return False
    return apiCall


def cleanup_audioRecord_apiCalls(apiCall):
    if (apiCall == "read" or apiCall == "getActiveMicrophones" or apiCall == "getAudioSource" 
            or apiCall == "startRecording"):
        return False
    return apiCall


def cleanup_clipboardTracking_apiCalls(apiCall):
    if (apiCall == "hasText" or apiCall == "getText"):
        return False
    return apiCall
"""

"""
def false_positive_cleanup():
    global extractedKeyloggerInfo, extractedCameraRecordingInfo, extractedClipboardTrackingInfo
    
    # Keylogger cleanup for getText(), AccessibilityNodeInfo and AccessibilityService
    foundKeyLoggerApiCalls = extractedKeyloggerInfo[0]
    foundKeyLoggerImports = extractedKeyloggerInfo[1]
    foundKeyLoggerPermissions = extractedKeyloggerInfo[2]
    if ("android.permission.BIND_ACCESSIBILITY_SERVICE" not in foundKeyLoggerPermissions):
        # Remove getEventType(), getAction(), getText() API calls from the list if BIND_ACCESSIBILITY_SERVICE is not declared
        foundKeyLoggerApiCalls[:] = [apiCall for apiCall in foundKeyLoggerApiCalls if cleanup_keylogger_accessibilityEvent_apiCalls(apiCall[2])]
        foundKeyLoggerApiCalls[:] = [apiCall for apiCall in foundKeyLoggerApiCalls if cleanup_keylogger_accessibilityNodeInfo_apiCalls(apiCall[2])]
        foundKeyLoggerImports[:] = [importClass for importClass in foundKeyLoggerImports if cleanup_keylogger_imports(importClass[2])]
    else:
        if ("android.view.accessibility.AccessibilityEvent" and "android.view.accessibility.AccessibilityNodeInfo" not in foundKeyLoggerImports):
            # Remove getEventType(), getAction(), getText() API calls from the list if both AccessibilityEvent and AccessibilityNodeInfo are not imported
            foundKeyLoggerApiCalls[:] = [apiCall for apiCall in foundKeyLoggerApiCalls if cleanup_keylogger_accessibilityEvent_apiCalls(apiCall[2])]
            foundKeyLoggerApiCalls[:] = [apiCall for apiCall in foundKeyLoggerApiCalls if cleanup_keylogger_accessibilityNodeInfo_apiCalls(apiCall[2])]
        elif ("android.view.accessibility.AccessibilityEvent" not in foundKeyLoggerImports):
            # Remove getEventType() and getAction() API calls if AccessibilityEvent class is not imported
            foundKeyLoggerApiCalls[:] = [apiCall for apiCall in foundKeyLoggerApiCalls if cleanup_keylogger_accessibilityEvent_apiCalls(apiCall[2])]
    extractedKeyloggerInfo[0] = foundKeyLoggerApiCalls
    extractedKeyloggerInfo[1] = [foundKeyLoggerImports]


    # Camera Recording cleanup for MediaRecorder start(), stop() and AudioRecord read()
    foundCameraRecordingApiCalls = extractedCameraRecordingInfo[0]
    foundCameraRecordingAPermissions = extractedCameraRecordingInfo[2]
    foundCameraRecordingImports = []
    for importClassTuple in extractedCameraRecordingInfo[1]:
        # Extract all import classes from tuple (Path, Package, Import Class, Line, Column) for list comprehension
        foundCameraRecordingImports.append(importClassTuple[2])
    if ("android.media.MediaRecorder" not in foundCameraRecordingImports or "android.permission.CAMERA" not in foundCameraRecordingAPermissions):
        # Remove MediaRecorder related API calls if required permission and class import are not present
        foundCameraRecordingApiCalls[:] = [apiCall for apiCall in foundCameraRecordingApiCalls if cleanup_camRecord_apiCalls(apiCall[2])]
    if ("android.media.AudioRecord" not in foundCameraRecordingImports or "android.permission.RECORD_AUDIO" not in foundCameraRecordingAPermissions):
        # Remove AudioRecord related API calls if required permission and class import are not present
        foundCameraRecordingApiCalls[:] = [apiCall for apiCall in foundCameraRecordingApiCalls if cleanup_audioRecord_apiCalls(apiCall[2])]
    extractedCameraRecordingInfo[0] = foundCameraRecordingApiCalls


    # Clipboard Tracking cleanup for hasText() and getText()
    foundClipboardTrackingApiCalls = extractedClipboardTrackingInfo[0]
    foundClipboardTrackingImports = []
    for importClassTuple in extractedClipboardTrackingInfo[1]:
        # Extract all import classes from tuple (Path, Package, Import Class, Line, Column) for list comprehension
        foundClipboardTrackingImports.append(importClassTuple[2]) 
    if ("android.content.ClipboardManager" not in foundClipboardTrackingImports):
        # Retain hasText() and getText() only if required class import is present
        foundClipboardTrackingApiCalls[:] = [apiCall for apiCall in foundClipboardTrackingApiCalls if cleanup_clipboardTracking_apiCalls(apiCall[2])]
    extractedClipboardTrackingInfo[0] = foundClipboardTrackingApiCalls
"""


# Main runner function
def scan_spyware(folderPath, xmlDoc, outputFile):
    hasException = False
    find_permissions(xmlDoc)

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

    # false_positive_cleanup()

    if hasException:
        print(Fore.YELLOW + "Some results have been ommitted due to exceptions")

    print_result(outputFile)