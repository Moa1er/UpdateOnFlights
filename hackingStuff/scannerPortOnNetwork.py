#!/bin/python3

import sys, socket
from datetime import datetime

#Define our target
if len(sys.argv) == 2:
	target = socket.gethostbyname(sys.argv[1]) #Translate a host name to IPV4
else:
	print('Invalid amount of arguments.')
	print('Syntax: python3 scanner.py <ip>')
	sys.exit()

#Add a pretty banner
print("-" * 50)
print("Scanning target " + target)
print("Time started " + str(datetime.now()))
print("-" * 50)

try:
	for port in range(0, 10000):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPV4 and SOCK_STREAM = PORT
		socket.setdefaulttimeout(1) #is a float
		result = s.connect_ex((target, port)) # returns error indicator
		#print("Checking port {}".format(port))
		if result == 0:
			print("Port {} is open".format(port))
		s.close()
		
except KeyboardInterrupt:
	print("\n Exiting program.")
	sys.exit()
except socket.gaierror:
	print('Hostname could not be resolved')
	sys.exit()
except socket.error:
	print("Couldn't connect to server.")
	sys.exit()
	
			
