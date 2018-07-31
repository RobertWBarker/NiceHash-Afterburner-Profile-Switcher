import json
import time
import subprocess
import APIRequests
import NiceHashAlgoID

from colorama import init
init()

#Default Varibles, to be overwritten
intervalTime = 10
profile1 = "MSIAfterburnerProfile1"
profile2 = "MSIAfterburnerProfile2"
excavatorAddress = ("127.0.0.1", "5100")

previousAlgID = None
currentAlgID = None
print("\033[2J\033[1;1f", end="") #Clears screen
print ("\033[32m" + "Starting Algorithm Monitor v0.1" + "\033[39m")

#Check that MSIAfterburnerProfile1 and MSIAfterburnerProfile2 are found in task Scheduler
try:
	subprocess.check_call([r"C:\Windows\System32\schtasks.exe", "/Query", "/TN", profile1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
	subprocess.check_call([r"C:\Windows\System32\schtasks.exe", "/Query", "/TN", profile2], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
except subprocess.CalledProcessError:
	print("\033[31m" + "Error locating task scheduler actions" + "\033[39m", end="")
	print(" May result in problems changing MSI Afterburner profiles")

while True:
	currentTime = time.strftime("%X", time.localtime())
	#localAPI
	localData = APIRequests.jsonFromTCP(excavatorAddress,{ "id":1, "method":"algorithm.list", "params":[] })

	try:
		currentAlgID = localData["algorithms"][0]["algorithm_id"]
		#print(NiceHashAlgoID.Dict[currentAlgID])
	except IndexError:
		print("\033[k", end="")
		print("\033[36m" + "Algorithm: " + "\033[31m" + "Error accessing local API" + "\033[39m", end="")
		print("\033[36m" + " Last check: " + "\033[39m" + currentTime, end="\r")
		time.sleep(intervalTime)
		continue

	if (previousAlgID != currentAlgID) and (previousAlgID != None) : #Never enters the loop
		print("[" + currentTime + "]", end=" ")
		print("Algorithm changed from " + NiceHashAlgoID.Dict[previousAlgID] + " to " + NiceHashAlgoID.Dict[currentAlgID])
		if currentAlgID == 20 :
			#low power mode
			subprocess.Popen([r"C:\Windows\System32\schtasks.exe", "/RUN", "/TN", profile2], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
			print("\033[35m" + "Changing MSIAfterburner to Low Power Mode" + "\033[39m")
		if currentAlgID != 20 and previousAlgID == 20:
			#High power mode
			subprocess.Popen([r"C:\Windows\System32\schtasks.exe", "/RUN", "/TN", profile1], shell=False, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
			print("\033[35m" + "Changing MSIAfterburner to High Power Mode" + "\033[39m")
	previousAlgID = currentAlgID
	print("\033[k", end ="")
	print("\033[36m" + "Algorithm: " + "\033[39m" + NiceHashAlgoID.Dict[currentAlgID], end="")
	print("\033[36m" + " Last check: " + "\033[39m" + currentTime, end="\r")

	time.sleep(intervalTime)
