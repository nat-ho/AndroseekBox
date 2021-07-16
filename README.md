# AndroseekBox

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

This document serves to provie a simple user guide for the tool. If you wish to find our more about the design choices 
behind `AndroseekBox`, please head to the [Developer Guide].

<br>

## Prequisites

In order to use `AndroseekBox`, you must have:

- Python preferably running version 3.8 or above

<br>

## Installation

- Install the necessary packages found in `requirements.txt`
    ```
    pip install -r requirements.txt
    ```

<br>

## Usage

- `AndroseekBox` only accepts Android APKs or XML Manifest files for its analysis.

- The directory `/AndroseekBox/OutputAPKs` will be created to hold all the decompiled APK files which have been analysed 
previously. 

- Inside the directory, each APK will reside in its own subdirectory that containns its source code and resources such as `AndroidManifest.xml` and `META-INF`

- Users who wish to re-unpack an APK file can do so by running it with `AndroseekBox` again.

- A sample of `/AndroseekBox/OutputAPKs` is displayed below
    ```
    /AndroseekBox/OutputAPKs
    ├── MalwareSample1
    │   ├── resources
    │   │   ├── AndroidManifest.xml
    │   │   ├── classes.dex
    │   │   ├── META-INF
    │   │   └── res
    │   │
    │   └── sources
    │       ├── android
    │       ├── androidx
    │       └── com
    │  
    └── MalwareSample2
    ```
<br>

## Example

- To start the analysis with an Android APK file:
    ```
    python AndroseekBox.py MalwareSample1.apk
    ```

    ![Initial analysis results](/docs/images/Result_InitialAnalysis.png)

<br>

- To select a malware module for static analysis, simply type in the desired module number shown:

    ![Results from static analysis](/docs/images/Result_moduleSection.png)