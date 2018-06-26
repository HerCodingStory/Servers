#UDPClient.py
import time
import sys
from socket import *

# Check command line arguments
if len(sys.argv) != 3: # system argument vector size has to be 3, if not equal to 3 close system
    print("Usage: python UDPClient <server ip address> <server port no>")
    sys.exit()

# Create a UDP socket using SOCK_DGRAM
clientSocket = socket(AF_INET, SOCK_DGRAM)

#Set the waiting time of one second for response
clientSocket.settimeout(1)

#Declare the server's socket address
remoteAddress = (sys.argv[1], int(sys.argv[2]))

for ping in range(10):
    sendTime = time.time() # set time
    message = "Ping " + str(ping + 1) + " " + str(time.strftime("%H:%M:%S")) # strftime = format string
    clientSocket.sendto(message.encode(), remoteAddress)
    # information about how long each response took
    try:
        message, server = clientSocket.recvfrom(1024)
        receivedTime = time.time()
        roundTripTime = receivedTime - sendTime
        print("Message Received", message)
        print("Round Trip Time\n", roundTripTime)
    except timeout:
        print("REQUEST TIMED OUT\n")

clientSocket.close()
