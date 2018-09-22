# NiceHash Afterburner automatic profile switcher

- [Introduction](#introduction)
- [Rational](#rational)
- [Setup](#setup)
- [How to run](#run)
- [Acknowledgments](#Acknowledgments)


# <a name="introduction"></a>Introduction
Script used to detect a change in mining algorithm and adjust MSI afterburner profile to maximize profits.<br />
<br />
<img src="Resources/NHAPS Screenshot.PNG" />

Script tested with:<br />
NiceHash version 2.0.2.6 - Beta<br />
Excavator API version 0.1.7<br />
MSI Afterburner 4.5.0<br />
Python version 3.6.5<br />
Operating system Windows 10<br />
<br />
.exe complied with:<br />
PyInstaller<br />


# <a name="rational"></a> Rational
The python script checks queries the local Excavator API for the current algorithm's ID number. After each check the ID is compared to the previous ID. If the script identifies a change in mining algorithm, a second check is ran to determine which MSI Afterburner profile that should be run. If a profile change is required the script automatically switches to the correct profile.

With daggerhashimoto being run so frequently this summer I realized I shouldn't be running at such a high power limit all the time. So while mining ethereum a low power profile will be run, but if the algorithm switches away from ethereum mining I wanted my power limit to jump back up. The script allows MSI Afterburner profiles to be selected based on the current algorithm being mined.


**Running MSI Afterburner without UAC prompts**

For this script to be run correctly MSI Afterburner has to be run, however, each time the program switches profiles the user is prompted to allow the program to make changes. Having click yes every time the script switches algorithms would ruin the automatic part of the applications. Therefore to circumvent the UAC prompt there are two options: Turn off UAC completely, which I've chosen not to do, and use Task Scheduler to run MSI Afterburner profile changes with elevated privileges.


# <a name="setup"></a> Setup
## Run as admin
Or
## Use Task Scheduler to launch MSI Afterburner without a UAC prompt
To accomplish this I followed a guide by digitalcitizen
[How To Use The Task Scheduler To Launch Programs Without UAC Prompts](https://www.digitalcitizen.life/use-task-scheduler-launch-programs-without-uac-prompts)

The tasks must be labeled "MSIAfterburnerProfile1" and "MSIAfterburnerProfile2". Profile 2 is running my profile for daggerhashimoto and profile 1 is for everything else.

**Action Triggers are set to**<br />
MSIAfterburnerProfile1<br />
Action: Start a program<br />
Program/script: "C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe"<br />
Add arguments (optional): -Profile1<br />
<br />
MSIAfterburnerProfile2<br />
Action: Start a program<br />
Program/script: "C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe"<br />
Add arguments (optional): -Profile2<br />


# <a name="run"></a> How to run?
The .exe can be run with administrator privileges, or after setting up the two actions through taskscheduler the .exe can be run as normal. The software must be run locally. It is possible to run the python script directly using python3.

# <a name="Acknowledgments"></a> Acknowledgments
GitHub User [YoRyan](https://github.com/YoRyan) - code used to read excavator API over TCP
