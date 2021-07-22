# AndroseekBox Developer Guide

`AndroseekBox` is a `Python` tool that aids in static analysis of Android APK files for malware detection.

With the pervasive and unrelating threat of increasing mobile malware, reverse engineering and static analysis will only 
continue to grow in importance. However, this process is a time consuming one and it is often easy to go down a rabbit 
hole looking at code not related to the problem. Malware developers are using tools such as ProGuard to obfuscate source 
code making it harder to analyse even when decompiled.

`AndroseekBox` attempts to help address some of these issues by automating processes such as extracting APK information, 
app components, URLs and IP addresses found in the source code. It also has static analysis `modules` that identify 
common API calls and permissions used for the different malware categories found in [Google Play Protect](https://developers.google.com/android/play-protect/phacategories). Built with a modular approach that is easy 
add on or modify, this tool aims to greatly reduce the time and effort needed to conduct static analysis so that you can 
focus on uncovering information in the right areas.

This developer guide will cover the rationale behind the design of `AndroseekBox` and its implementation details. 
Please read through the [User Guide](README.md) before you start on this document as it provides an introduction to the 
usage and examples.

<br>

## Tools Used

An overview of the main libraries used in `AndroseekBox`:

- [jadx](https://github.com/skylot/jadx)
- [javalang](https://github.com/c2nes/javalang)

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

### Phase 1: Pre-process and decompile ( `xmlUtils.py` )
`AndroseekBox.py` will determine the input file type and process it accordingly.
- If an APK file is received, it first uses `jadx` to decompile the APK into Java.
- The `AndroidManifest.xml` file is then parsed using to identify application details such as Name and Target SDK.
- Application components, string resources and deeplinks are also then parsed and printed .

### Phase 2: Scanning of Java source code ( `apkUtils.py` )
- The decompiled Java files will then be scanned to identify URL and IP addresses, as well as Native Libraries loaded and Native Methods.
- These results will also be presented to the user.

### Phase 3: Static Analysis (`modules`)
- Available malware modules will be presented to users to select which malware category should the analysis target.
- Each module has a main runner function which calls the other respective functions to identify API calls, Class imports and permission common for the selected malware category.
- `javalang` is used to parse the code into an Abstract Syntax Tree for precise identification of API calls and Imports.
- Results will then be presented to users which also include file path, package name, line and column of identified information.

<br>

## Design Considerations

### Modular approach for static analysis 

The initial version of `AndroseekBox.py` contained a single function that executed checks from a list of generic dangerous permissions and common API calls found in malware. As the list grew, it became extremely hard to maintain and stability of the tool was affected. Further testing also revealed that many of the results returned were false positives.

To address these issues, the checks were broken down into different modules based on some of Google's Play Protect Android malware categories. Users could now execute targeted analysis with more refined checks that also included false positive data cleaning functions. This in turn results in more accurate and actionable information that will be useful for analysts to quickly identify areas concern to dig deeper. These design choices also led to increased understandability of code and maintainability as the different modules were easy to add, remove and modify.

### Use of `javalang` parser

Regular Expression (RegEx) was used in the beginning to identify class imports and API calls, however further development showed that use of RegEx was not reliable for all scenarios and required significant resources to maintain new or updated API calls. 

As accuracy and ease of maintenance were key considerations when developing the tool in order to keep up with the every changing threat landscape, `javalang` Parser was selected as the optimal solution. Java code will be parsed into Abstract Syntax trees (AST) which allows easy filtering and precise identification of class imports and method invocations.

<br>

## Acknowledgement 

Project inspiration take from [AndroPyTool](https://github.com/alexMyG/AndroPyTool) and [medusa](https://github.com/Ch0pin/medusa)