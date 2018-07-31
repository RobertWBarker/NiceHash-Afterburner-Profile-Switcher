import requests
import socket
import json

def jsonFromURL(url):
	try:
		response = requests.get(url).json()
	except Exception as e:
		print("Error using API: {0:s}".format(str(e)))
		return None
	return response

def jsonFromTCP(address, command): #Ex. jsonFromTCP(('127.0.0.1', '5100'),{ "id":1, "method":"algorithm.list", "params":[] }))
	EXCAVATOR_ADDRESS = address
	EXCAVATOR_TIMEOUT = 10
	BUF_SIZE = 1024
	#command = { "id":1, "method":"algorithm.list", "params":[] }
	s = socket.create_connection(EXCAVATOR_ADDRESS, EXCAVATOR_TIMEOUT)
	# send newline-terminated command
	s.sendall((json.dumps(command).replace('\n', '\\n') + '\n').encode())
	response = ''
	while True:
	    chunk = s.recv(BUF_SIZE).decode()
	    # excavator responses are newline-terminated too
	    if '\n' in chunk:
	        response += chunk[:chunk.index('\n')]
	        break
	    else:
	        response += chunk
	s.close()

	response_data = json.loads(response)
	return response_data
