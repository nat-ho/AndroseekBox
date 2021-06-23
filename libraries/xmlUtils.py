import subprocess
from xml.dom import minidom
import xml.etree.ElementTree as tree

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