import os
import re
from threading import Thread


apiRegexList = ["sendMultimediaMessage(.*)", "sendMultipartTextMessage(.*)", "sendTextMessage(.*)", "sendTextMessageWithoutPersisting(.*)"]
importRegexList = ["android.telephony.SmsManager", "android.telephony.SmsMessage"]
permissionRegexList = ["android.permission.READ_SMS", "android.permission.RECEIVE_SMS", "android.permission.SEND_SMS"]

foundApiList = []
foundPermissionList = []
foundImportList = []

#Todo: Function to extract API calls and imports (location and line number)

#Todo: Function to rxtract permissions from XML and possibly in classes

#Todo: Function to print results

#Todo: Runner function with threading if necessary
def scan_sms_fraud(folderPath):
    pass