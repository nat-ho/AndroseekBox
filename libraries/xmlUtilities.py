import subprocess
from xml.dom import minidom
from xml.etree import ElementTree

def parse_xml(xml):
    return minidom.parse(xml)


def get_attribute(xmlDoc, node, attribute):
    node = xmlDoc.getElementsByTagName(node)

    for atr in node:
        if (len(atr.getAttribute(attribute)) > 0):
            return atr.getAttribute(attribute)


def get_exported_components(xmlDoc):
    components = ["activity", "activity-alias", "service", "receiver", "provider"]
    exportedComponents = []

    for component in components:
        node = xmlDoc.getElementsByTagName(component)

        for atr in node:
            if "true" in atr.getAttribute("android:exported"):
                exportedComponents.append(component + ": \t" + atr.getAttribute("android:name"))
            
            elif atr.getElementsByTagName("intent-filter") and atr.getAttribute("android:name") not in exportedComponents:
                exportedComponents.append(component + ": \t" + atr.getAttribute("android:name"))

    return exportedComponents