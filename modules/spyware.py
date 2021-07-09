import javalang
from threading import Thread
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


extractedScreenCaptureInfo = [[] for i in range(3)]
extractedDeviceReconInfo = [[] for i in range(3)]
extractedKeyloggerInfo = [[] for i in range(3)]
extractedSLocationTrackingInfo = [[] for i in range(3)]
extractedCameraRecordingInfo = [[] for i in range(3)]
extractedClipboardTrackingInfo = [[] for i in range(3)]

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

# KEYLOGGER
# getText: Detects if Accessibility Service is used in conjunction with getText() method which can be used to log keystrokes to the console
# https://stackoverflow.com/questions/27245185/android-key-logger
keyloggerImports = {
    "android.view.accessibility.AccessibilityNodeInfo", "android.accessibilityservice.AccessibilityService"
}
keyloggerAPIs = {
    "getText"
}
keyloggerPermissions = {
    "android.permission.BIND_ACCESSIBILITY_SERVICE"
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

# CAMERA RECORDING MONITORS
# setAudioSource & setVideoSource: Sets video and audio source used for recording
# setOutputFile: Sets file object to be written during recording
# prepare & start & stop: Controls capturing and encoding of data
# getSurface: Retrieves surface object from MediaRecorder
# read: Audio data is being read
# getActiveMicrophones: Retrieve active microphones
# getAudioSource: Returns the audio recording source
# startRecording & stop: Start/stop device audio recording from the AudioRecord instance
cameraRecordingImports = {
    "android.media.MediaRecorder", "android.media.AudioRecord"
}
cameraRecordingAPIs = {
    "setAudioSource", "setVideoSource", "setOutputFile", "prepare", "start", "stop", "getSurface", "read", 
    "getActiveMicrophones", "getAudioSource", "startRecording", "stop"
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


def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member in screenCaptureAPIs):
                extractedScreenCaptureInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in deviceReconAPIs):
                extractedDeviceReconInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in keyloggerAPIs):
                extractedKeyloggerInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in locationTrackingAPIs):
                extractedSLocationTrackingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in cameraRecordingAPIs):
                extractedCameraRecordingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))
            elif (node.member in clipboardTrackingAPIs):
                extractedClipboardTrackingInfo[0].append((filePath, packageName, node.member, node.position.line, node.position.column))

    except Exception as e:
        print("Exception occured when parsing {} for API calls : :{}".format(filePath, e))


def find_imports(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.Import):
            if (node.path in screenCaptureImports):
                extractedScreenCaptureInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in deviceReconImports):
                extractedDeviceReconInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in keyloggerImports):
                extractedKeyloggerInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in locationTrackingImports):
                extractedSLocationTrackingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in cameraRecordingImports):
                extractedCameraRecordingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))
            elif (node.path in clipboardTrackingImports):
                extractedClipboardTrackingInfo[1].append((filePath, packageName, node.path, node.position.line, node.position.column))

    except Exception as e:
        print("Exception occured when parsing {} for imported classes : :{}".format(filePath, e))


def find_permissions(xmlDoc):
    try:
        tempPermissionList = get_attribute_list(xmlDoc, "uses-permission", "android:name")

        for permission in tempPermissionList:
            if (permission in screenCapturePermissions):
                extractedScreenCaptureInfo[2].append(permission)
            elif (permission in deviceReconPermissions):
                extractedDeviceReconInfo[2].append(permission)
            elif (permission in keyloggerPermissions):
                extractedKeyloggerInfo[2].append(permission)
            elif (permission in locationTrackingPermissions):
                extractedSLocationTrackingInfo[2].append(permission)
            elif (permission in cameraRecordingPermissions):
                extractedCameraRecordingInfo[2].append(permission)

    except Exception as e:
        print("Exception occured when parsing Android Manifest XML for permissions requested : :{}".format(e))


def print_list(info, type):
    print("-" * 20 + type + "-" * 20)
    filteredInfo = list(set(info))
    for info in filteredInfo:
        print(info)


def print_all_information(extractedInfo):
    for category, info in enumerate(extractedInfo):
        if category == 0:
            print_list(info, "Related API Calls")
        elif category == 1:
            print_list(info, "Related Class Imports")
        elif category == 2:
            print_list(info, "Related Permissions")
    else:
        print("No related API calls were found for screen capture")        


def print_result():
    global extractedScreenCaptureInfo, extractedDeviceReconInfo, extractedKeyloggerInfo, extractedSLocationTrackingInfo, extractedCameraRecordingInfo, extractedClipboardTrackingInfo

    # print("\n---------------------Related API Calls---------------------")
    print("\nAPI calls related to screen capture Spyware")
    if (extractedScreenCaptureInfo):
        print_all_information(extractedScreenCaptureInfo)
    else:
        print("No related API calls were found for screen capture")

    print("\nAPI calls related to device recon Spyware")
    if (extractedDeviceReconInfo):
        print_all_information(extractedDeviceReconInfo)
    else:
        print("No related API calls were found for device recon")

    print("\nAPI calls related to keylogger Spyware")
    if (extractedKeyloggerInfo):
        print_all_information(extractedKeyloggerInfo)
    else:
        print("No related API calls were found for keylogger")

    print("\nAPI calls related to location tracking Spyware")
    if (extractedSLocationTrackingInfo):
        print_all_information(extractedSLocationTrackingInfo)
    else:
        print("No related API calls were found for location tracking")

    print("\nAPI calls related to camera recording Spyware")
    if (extractedCameraRecordingInfo):
        print_all_information(extractedCameraRecordingInfo)
    else:
        print("No related API calls were found for camera recording")

    print("\nAPI calls related to clipboard tracking Spyware")
    if (extractedClipboardTrackingInfo):
        print_all_information(extractedClipboardTrackingInfo)
    else:
        print("No related API calls were found for clipboard tracking")

    # print("\n---------------------Related API Calls---------------------")
    # if (foundApiList):
    #     print("\nList of API calls related to SMS fraud found in the application:")

    #     for apiCallCount, apiCall in enumerate(foundApiList):
    #         print("{}.\tFile Path: {}".format(apiCallCount+1, apiCall[0]))
    #         print("\tPackage: {}".format(apiCall[1]))
    #         print("\tAPI Call: {}".format(apiCall[2]))
    #         print("\tLine Number & Column Number: ({}, {})".format(apiCall[3], apiCall[4]))
    #         print("-" * 60)
    # else:
    #     print("No related API calls were found")

    # print("\n---------------------Related Library Imports---------------------")
    # if (foundImportList):
    #     print("\nList of class imports related to SMS fraud found in the application:")

    #     for importCount, classImport in enumerate(foundImportList):
    #         print("{}.\tFile Path: {}".format(importCount+1, classImport[0]))
    #         print("\tPackage: {}".format(classImport[1]))
    #         print("\tImport: {}".format(classImport[2]))
    #         print("\tLine Number & Column Number: ({}, {})".format(classImport[3], classImport[4]))
    #         print("-" * 60)
    # else:
    #     print("No related class imports were found")

    # print("\n---------------------Related Permissions Declared---------------------")
    # if (foundPermissionList):
    #     print("\nList of permissions related to SMS fraud found in the application:")

    #     for permissionCount, permission in enumerate(foundPermissionList):
    #         # print("-" * 40)
    #         print("{}.\t{}".format(permissionCount+1, permission))
    #     print("-" * 60)
    # else:
    #     print("No related permissions were found")


def scan_spyware(folderPath, xmlDoc):
    hasException = False
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
        
    find_permissions(xmlDoc)
    
    if hasException:
        print("Some results have been ommitted due to exceptions")
    print_result()