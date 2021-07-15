from xml.dom import minidom
import colorama
from colorama import init, Fore, Style
import xml.etree.ElementTree as tree

def parse_xml(xml):
    return minidom.parse(xml)


def get_attribute(xmlDoc, node, attribute):
    node = xmlDoc.getElementsByTagName(node)

    for atr in node:
        if (len(atr.getAttribute(attribute)) > 0):
            return atr.getAttribute(attribute)


def get_attribute_list(xmlDoc, node, attribute):
    attributes = []
    node = xmlDoc.getElementsByTagName(node)

    for atr in node:
        attributes.append(atr.getAttribute(attribute))

    return attributes


def get_app_components(xmlDoc):
    components = ["activity", "activity-alias", "service", "receiver", "provider"]
    applicationComponents = []

    for component in components:
        node = xmlDoc.getElementsByTagName(component)

        for atr in node:
            fullComponentName = component + ": \t" + atr.getAttribute("android:name")
            if "true" in atr.getAttribute("android:exported"):
                applicationComponents.append((fullComponentName,"Exported"))
            
            elif atr.getElementsByTagName("intent-filter") and atr.getAttribute("android:name") not in applicationComponents:
                applicationComponents.append((fullComponentName,"Exported"))
            else:
                applicationComponents.append((fullComponentName,"notExported"))

    return applicationComponents


def parse_xml_strings(xmlDoc):
    strings = []

    stringsXML = tree.parse(xmlDoc)
    root = stringsXML.getroot()

    for child in root.iter():
        if child.tag == "string" and child.attrib["name"] is not None and child.text is not None:
            attribute = child.attrib["name"]
            text = child.text
            strings.append(child.attrib["name"] + " = " + child.text)
    return strings


#Taken from https://github.com/Ch0pin/medusa/blob/master/libraries/xmlUtils.py
def get_deeplinks(xmlDoc):
    
    deeplinksTree = {}
    
    activityNodes = xmlDoc.getElementsByTagName("activity")
    activityNodes += xmlDoc.getElementsByTagName("activity-alias")
    for act in activityNodes:
        intent_filter = act.getElementsByTagName("intent-filter")
        deeplinks = []
        for i in range(0,intent_filter.length):
            schemes = []
            hosts = []
            paths = []
            patterns = []
            pathPrefixes = []
            port = ""


            for data in intent_filter.item(i).getElementsByTagName("data"):
                if data.hasAttribute("android:scheme") and data.hasAttribute("android:host"): #scenario 1
                    scheme = data.getAttribute("android:scheme")
                    deeplink = scheme + "://"
                    deeplink += data.getAttribute("android:host")
                    if data.hasAttribute("android:port"):
                        deeplink += ":" + data.getAttribute("android:port")        
                    if data.hasAttribute("android:path"):
                        deeplink += data.getAttribute("android:path")
                    if data.hasAttribute("android:pathPattern"):
                        deeplink += data.getAttribute("android:pathPattern")
                    if data.hasAttribute("android:pathPrefix"):
                            deeplink += data.getAttribute("android:pathPrefix")
                    #print(deeplink)
                    deeplinks.append(deeplink)

                elif data.hasAttribute("android:scheme") and not data.hasAttribute("android:host"): #scenario 2
                    schemes.append(data.getAttribute("android:scheme"))
                elif not data.hasAttribute("android:scheme"):
                    if data.hasAttribute("android:host"):
                        hosts.append(data.getAttribute("android:host"))
                    elif data.hasAttribute("android:port"):
                        port =data.getAttribute("android:port")  
                    elif data.hasAttribute("android:path"):
                        paths.append(data.getAttribute("android:path"))
                    elif data.hasAttribute("android:pathPattern"):
                        patterns.append(data.getAttribute("android:pathPattern"))
                    elif data.hasAttribute("android:pathPrefix"):
                        pathPrefixes.append(data.getAttribute("android:pathPrefix"))
                
            for schm in schemes: 
                deeplink = schm + "://"
                for hst in hosts:
                    deeplink = schm + "://"
                    deeplink += hst
                    if port != "":
                        deeplink = deeplink + ":" + port
                    for path in paths:
                        deeplink += path
                    for pattern in patterns:
                        deeplink += pattern
                    for pathPrefix in pathPrefixes:
                        deeplink += pathPrefix
                    #print(deeplink)
                    deeplinks.append(deeplink)


                #print(deeplink)
                deeplinks.append(deeplink)
            if deeplinks:
                deeplinksTree[act.getAttribute("android:name")] = deeplinks

    return deeplinksTree


def print_deepLinks_map(deeplinks_r):
        deeplinks = deeplinks_r
        a = 0
        print(Fore.CYAN + Style.BRIGHT + "\n" + "-" * 40 + "DeepLinks Map" + "-" * 40 + ":")
        try:
            for key in deeplinks:
                print("Deeplinks that trigger: " + key)
                for value in deeplinks[key]:
                    #deeplinks.append(value)
                    print("\t|-> " + value)
                    a = a+1
            print(Fore.CYAN + Style.BRIGHT + "-" * 38 + "Total Deeplinks:{}".format(a) + "-" * 38 + "|")
        except Exception as e:
            print(e)