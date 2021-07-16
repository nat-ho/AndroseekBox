# AndroseekBox Developer Guide

`AndroseekBox` is a `Python` tool that aids in static analysis of Android APK files for malware detection.

With the pervasive and unrelating threat of increasing mobile malware, reverse engineering and static analysis will only 
continue to grow in importance. However, this proccess is a time consuming one and it is often easy to go down a rabbit 
hole looking at code not related to the problem. Malware developers are using tools such as ProGuard to obfuscate source 
code making it harder to analyse even when decompiled.

`AndroseekBox` attempts to help address some of these issues by automating processes such as extrating APK information, 
app components, URLs and IP addresses found in the source code. It also has static analysis `modules` that identify 
common API calls and permissions used for the different malware categories found in Google Play Protect 
(https://developers.google.com/android/play-protect/phacategories#spyware). Built with a modular approach that is easy 
add on or modify, this tool aims to greatly reduce the time and effort needed to conduct static analysis so that you can 
focus on uncovering information in the right areas.

This developer guide will cover the rationale behind the design of `AndroseekBox` and it's implementation details. 
Please read through the [User Guide](README.md) before you start on this document as it provides an introduction to the 
usage and examples.

<br>

## Tools Used

An overview of the main tools used in `AndroseekBox`:

- `jadx`
- `javalang`

<br>

## Project Structure

Below is the overall code structure of the project:

```
.
├── dependencies
│   └── jadx
├── libraries
│   ├── apkutils.py
│   └── xmlUtils.py
├── modules
│   ├── backdoor.py
│   ├── click_fraud.py
│   ├── sms_fraud.py
│   └── spyware.py
├── docs
└── AndroseekBox.py
```

### `AndroseekBox.py`
The main logic responsible for running the tool resides in this file which determines the flow of code depending on input file and handles printing of APK information.

<br>

### Phase 1: Preprocess and decompile ( `xmlUtils.py` )
`AndroseekBox.py` will determine the input file type and process it accordingly.
- If an APK file is received, it first uses `jadx` to decompile the APK into Java.
- The `AndroidManifest.xml` file is then parsed using to identify application details such as Name and Taget SDK.
- Application components, string resources and deeplinks are also then parsed and printed .

### Phase 2: Scanning of Java source code ( `apkUtils.py` )
- The decompiled Java files will then be scanned to identify URL and IP addresseses, as well as Native Libraries loaded and Native Methods.
- These results will also be presented to the user.

### Phase 3: Static Analysis (`modules`)
- Availble malware modules will be presented to users to select which malware category should the analysis target.
- Each module has a main runner function which calls the other respective functions to idenify API calls, Class imports and permission common for the selected malware category.
- `javalang` is used to parse the code into an Abstract Syntax Tree for precise identification of API calls and Imports.
- Results will then be presented to users which also include file path, package name, line and column of identified information.

<br>

## Design Considerations

### Modular approach for static analysis

### Use of `javalang` parser

<br>

## Acknowledgement 

Project inspiration take from [AndroPyTool](https://github.com/alexMyG/AndroPyTool) and [medusa](https://github.com/Ch0pin/medusa)