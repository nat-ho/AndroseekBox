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
keyloggerImports = {
    "android.media.MediaRecorder", "android.media.AudioRecord"
}
keyloggerAPIs = {
    "setAudioSource", "setVideoSource", "setOutputFile", "prepare", "start", "stop", "getSurface", "read", 
    "getActiveMicrophones", "getAudioSource", "startRecording", "stop"
}
keyloggerPermissions = {
    "android.permission.CAMERA", "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.RECORD_AUDIO"
}

# CLIPBOARD INFORMATION TRACKING - No permission required to register a listener that can transmit device's clipboard to a remote server
# hasPrimaryClip: App is checking if clipboard contains data
# getPrimaryClip: App is retrieving text from the clipboard
# hasText: Deprecated method since API level 11 for hasPrimaryClip()
# getText: Deprecated method since API level 11 for getPrimaryClip()
clipboardImports = {
    "android.content.ClipboardManager"
}
clipboardAPIs = {
    "hasPrimaryClip", "getPrimaryClip", "hasText", "getText"
}