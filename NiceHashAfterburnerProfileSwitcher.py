import json
import time
import subprocess
import APIRequests
import NiceHashAlgoID

import ctypes, sys

from colorama import init
init()

def main():

	#Default Varibles, to be overwritten
	intervalTime = 10
	profile1 = "MSIAfterburnerProfile1"
	profile2 = "MSIAfterburnerProfile2"
	MSIApplicationLocation = r"C:\Program Files (x86)\MSI Afterburner\MSIAfterburner.exe"
	excavatorAddress = ("127.0.0.1", "5100")

	previousAlgID = None
	currentAlgID = None

	elevatedPrivileges = isUserAdmin()
	scheduleTasksPresent = hasScheduledTasks(profile1, profile2)

	print("\033[2J\033[1;1f", end="") #Clears screen
	print ("\033[32m" + "Starting Algorithm Monitor v0.2" + "\033[39m")

	if elevatedPrivileges == True:
		print("\033[36m" + "Running in Admin Mode" + "\033[39m")
	elif scheduleTasksPresent == True:
		print("\033[33m" + "Application is not being run as Admin" + "\033[39m")
		print("Changing profiles using task scheduler MSI Afterburner profiles")
	else:
		print("\033[31m" + "Not running as admin and unable to locate task scheduler actions" + "\033[39m")
		print("May result in inability to change MSI Afterburner profiles")

	#Main Loop
	while True:
		currentTime = time.strftime("%X", time.localtime())
		#localAPI
		try:
		    localData = APIRequests.jsonFromTCP(excavatorAddress,{ "id":1, "method":"algorithm.list", "params":[] })
		except socket.error as error:
			print("\033[k", end="")
			print("\033[36m" + "Algorithm: " + "\033[31m" + "Error accessing local API" + "\033[39m", end=" ")
			print("\033[36m" + "Last check: " + "\033[39m" + currentTime, end="\r")
			time.sleep(intervalTime)
			continue

		try:
			currentAlgID = localData["algorithms"][0]["algorithm_id"]
			#print(NiceHashAlgoID.Dict[currentAlgID])
		except IndexError:
			print("\033[k", end="")
			print("\033[36m" + "Algorithm: " + "\033[33m" + "API online, No mining detected" + "\033[39m", end=" ")
			print("\033[36m" + "Last check: " + "\033[39m" + currentTime, end="\r")
			time.sleep(intervalTime)
			continue

		if (previousAlgID != currentAlgID) and (previousAlgID != None) : #Never enters the loop
			print("[" + currentTime + "]", end=" ")
			print("Algorithm changed from " + NiceHashAlgoID.Dict[previousAlgID] + " to " + NiceHashAlgoID.Dict[currentAlgID])
			if currentAlgID == 20 :
				#Low power mode
				if elevatedPrivileges == True:
					subprocess.Popen([MSIApplicationLocation, "-profile2"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
				elif scheduleTasksPresent == True:
					subprocess.Popen([r"C:\Windows\System32\schtasks.exe", "/RUN", "/TN", profile2], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
				print("\033[k", end ="")
				print("\033[35m" + "Changing MSIAfterburner to Low Power Mode" + "\033[39m")
			if currentAlgID != 20 and previousAlgID == 20:
				#High power mode
				if elevatedPrivileges == True:
					subprocess.Popen([MSIApplicationLocation, "-profile1"], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
				elif scheduleTasksPresent == True:
					subprocess.Popen([r"C:\Windows\System32\schtasks.exe", "/RUN", "/TN", profile1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
				print("\033[k", end ="")
				print("\033[35m" + "Changing MSIAfterburner to High Power Mode" + "\033[39m")
		previousAlgID = currentAlgID
		print("\033[k", end ="")
		print("\033[36m" + "Algorithm: " + "\033[39m" + NiceHashAlgoID.Dict[currentAlgID], end=" ")
		print("\033[36m" + "Last check: " + "\033[39m" + currentTime, end="\r")

		time.sleep(intervalTime)


def isUserAdmin():
	#Checking that program is elevated to admin preivligegs to allow for MSIAfterburner to be run without UAC notification
	try:
	    return ctypes.windll.shell32.IsUserAnAdmin()
	except:
	    return False

def hasScheduledTasks(profile1, profile2):
	#Check that MSIAfterburnerProfile1 and MSIAfterburnerProfile2 are found in task Scheduler
	try:
		subprocess.check_call([r"C:\Windows\System32\schtasks.exe", "/Query", "/TN", profile1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		subprocess.check_call([r"C:\Windows\System32\schtasks.exe", "/Query", "/TN", profile2], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
		return True
	except: #subprocess.CalledProcessError:
		return False

if __name__ == "__main__":
    main()
