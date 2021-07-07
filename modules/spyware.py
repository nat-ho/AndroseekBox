import javalang
from threading import Thread
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


foundImportList = []
foundApiList = []
foundPermissionList = []

# SCREEN CAPTURE
# createScreenCaptureIntent: Creates an intent in order to start screen capture
# getMediaProjection: Retrieves MediaProjection obtained from successful capture request
screenCaptureImports = ["android.media.projection.MediaProjectionManager"]
screenCaptureAPIs = ["createScreenCaptureIntent", "getMediaProjection"]
screenCapturePermissions = ["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"]

# DEVICE RECON
# getLine1Number: Retrieve phone number of SIM card
# getSimOperator: Retrieve mobile country code and mobile network code of SIM provider
# loadClass("android.os.SystemProperties"): android.os.SystemProperties is a hidden class so this check determines if reflection was used to gain access and information about system properties
deviceReconImports = ["android.telephony.TelephonyManager"]
deviceReconAPIs = ["getLine1Number", "getSimOperator", "loadClass"] #Check if loading android.os.SystemProperties
deviceReconPermissions = ["android.permission.READ_PHONE_STATE", "android.permission.READ_SMS", "android.permission.READ_PHONE_NUMBERS"]

# KEYLOGGER
# getText: Detects if Accessibility Service is used in conjunction with getText() method which can be used to log keystrokes to the console
# https://stackoverflow.com/questions/27245185/android-key-logger
keyloggerImports = ["android.view.accessibility.AccessibilityNodeInfo", "android.accessibilityservice.AccessibilityService"]
keyloggerAPIs = ["getText"]
keyloggerPermissions = ["android.permission.BIND_ACCESSIBILITY_SERVICE"]

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
locationTrackingImports = ["android.location.LocationManager", "android.location.LocationListener", "android.location.Location", "com.google.android.gms.common.ConnectionResult", "com.google.android.gms.common.api.GoogleApiClient", "com.google.android.gms.location.LocationListener", "com.google.android.gms.location.LocationRequest", "com.google.android.gms.location.LocationServices", "android.telephony.TelephonyManager"]
locationTrackingAPIs = ["getLastKnownLocation", "getLastLocation", "onLocationChanged", "onProviderDisabled", "onStatusChanged", "getLatitude", "getLongitude", "getCallState", "getCallStateForSubscription", "isInCall",  "getDeviceId", "getImei", "loadClass"] #Check if loading android.os.SystemProperties
locationTrackingPermissions = ["android.permission.ACCESS_COARSE_LOCATION", "android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_BACKGROUND_LOCATION", "android.permission.READ_PHONE_STATE"]

#CAMERA RECORDING MONITORS
# setAudioSource & setVideoSource: Sets video and audio source used for recording
# setOutputFile: Sets file object to be written during recording
# getSurface: Retrieves surface object from MediaRecorder
# prepare & start & stop: Controls capturing and encoding of data
keyloggerImports = ["android.media.MediaRecorder", "android.media.AudioRecord", "android.content.ClipboardManager"]
keyloggerAPIs = ["setAudioSource", "setVideoSource", "setOutputFile", "prepare", "start", "stop"]
keyloggerPermissions = ["android.permission.CAMERA", "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.RECORD_AUDIO"]







apiCallsList = ["sendMultimediaMessage", "sendMultipartTextMessage", "sendTextMessage", "sendTextMessageWithoutPersisting"]
importList = ["android.telephony.SmsManager", "android.telephony.SmsMessage"]
permissionList = ["android.permission.READ_SMS", "android.permission.RECEIVE_SMS", "android.permission.SEND_SMS", "android.permission.READ_PHONE_STATE"]



def find_api_calls(filePath, sourcecode):
    try:
        tree = javalang.parse.parse(sourcecode)
        packageName = tree.package.name

        for path, node in tree.filter(javalang.tree.MethodInvocation):
            if (node.member in apiCallsList):
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


def find_permissions(xmlDoc):
    try:

        tempPermissionList = get_attribute_list(xmlDoc, "uses-permission", "android:name")

        for permission in tempPermissionList:
            if (permission in permissionList):
                foundPermissionList.append(permission)
    except Exception as e:
        print("Exception occured when parsing Android Manifest XML for permissions requested : :{}".format(e))


def print_result():
    global foundApiList, foundImportList, foundPermissionList
    foundApiList = list(set(foundApiList))
    foundImportList = list(set(foundImportList))

    print("\n---------------------Related API Calls---------------------")
    if (foundApiList):
        print("\nList of API calls related to SMS fraud found in the application:")

        for apiCallCount, apiCall in enumerate(foundApiList):
            print("{}.\tFile Path: {}".format(apiCallCount+1, apiCall[0]))
            print("\tPackage: {}".format(apiCall[1]))
            print("\tAPI Call: {}".format(apiCall[2]))
            print("\tLine Number & Column Number: ({}, {})".format(apiCall[3], apiCall[4]))
            print("-" * 60)
    else:
        print("No related API calls were found")

    print("\n---------------------Related Library Imports---------------------")
    if (foundImportList):
        print("\nList of class imports related to SMS fraud found in the application:")

        for importCount, classImport in enumerate(foundImportList):
            print("{}.\tFile Path: {}".format(importCount+1, classImport[0]))
            print("\tPackage: {}".format(classImport[1]))
            print("\tImport: {}".format(classImport[2]))
            print("\tLine Number & Column Number: ({}, {})".format(classImport[3], classImport[4]))
            print("-" * 60)
    else:
        print("No related class imports were found")

    print("\n---------------------Related Permissions Declared---------------------")
    if (foundPermissionList):
        print("\nList of permissions related to SMS fraud found in the application:")

        for permissionCount, permission in enumerate(foundPermissionList):
            # print("-" * 40)
            print("{}.\t{}".format(permissionCount+1, permission))
        print("-" * 60)
    else:
        print("No related permissions were found")


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