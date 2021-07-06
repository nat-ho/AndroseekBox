import javalang
from threading import Thread
from pathlib import Path
from libraries.xmlUtils import get_attribute_list


foundImportList = []
foundApiList = []
foundPermissionList = []

#Screen Capture
screenCaptureImports = ["android.media.projection.MediaProjectionManager"]
screenCaptureAPIs = ["createScreenCaptureIntent", "getMediaProjection"]
screenCapturePermissions = ["android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.READ_EXTERNAL_STORAGE"]

#Device Recon
deviceReconImports = ["android.telephony.TelephonyManager", "android.os.SystemProperties", "android.os.SystemProperties"]
deviceReconAPIs = ["getLine1Number", "getSimOperator", "getMethod"] #getMethod('get', String.class)
deviceReconPermissions = ["android.permission.READ_PHONE_STATE", "android.permission.READ_SMS", "android.permission.READ_PHONE_NUMBERS"]

#Keylogger
keyloggerImports = ["android.view.accessibility.AccessibilityNodeInfo", "android.accessibilityservice.AccessibilityService"]
keyloggerAPIs = ["getText"]
keyloggerPermissions = ["android.permission.BIND_ACCESSIBILITY_SERVICE"]

#Location Tracking
locationTrackingImports = ["android.location.LocationManager", "android.location.LocationListener", "android.location.Location", "android.telephony.TelephonyManager", "android.os.SystemProperties"]
locationTrackingAPIs = ["getLastKnownLocation", "onLocationChanged", "onProviderDisabled", "onStatusChanged", "getLatitude", "getLongitude", "getCallState", "getCallStateForSubscription", "isInCall",  "getDeviceId", "getImei", "getMethod"] #getMethod('get', String.class)
locationTrackingPermissions = ["android.permission.ACCESS_COARSE_LOCATION", "android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_BACKGROUND_LOCATION", "android.permission.READ_PHONE_STATE"]

#Camera Recording Monitors
keyloggerImports = ["android.media.MediaRecorderandroid.media.MediaRecorderandroid.media.MediaRecorder", "android.media.AudioRecord", "android.content.ClipboardManager"]
keyloggerAPIs = ["setCamera", "setAudioSource", "setOutputFile", "getSurface", "start", "stop"]
keyloggerPermissions = ["android.permission.CAMERA", "android.permission.WRITE_EXTERNAL_STORAGE", "android.permission.RECORD_AUDIO"]
