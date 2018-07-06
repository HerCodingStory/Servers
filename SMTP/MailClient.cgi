#!/usr/bin/python
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR
import socket
import time
import re
import binascii
import base64

# Contribution: Fernando helped me with the parsin

# Parsin
def parsin(query):
    parsed = {}
    if query:
        pairs = query.split('&')
        for pair in pairs:
            pairList = pair.split('=')
            value = re.sub(r'[+]', ' ', pairList[0])
            nameDecode = re.sub(r'%[0-9a-fA-F]{2}', convertASCII, value)
            value1 = re.sub(r'[+]', ' ', pairList[1])
            valueDecode = re.sub(r'%[0-9a-fA-F]{2}', convertASCII, value1)
            parsed[nameDecode] = valueDecode
    return parsed

def convertASCII(match):
    match = match.group()
    return binascii.unhexlify(match[1:3])

# Given From Downey
def send_recv(socket, msg, code):
    if msg != None:
        print "Sending==> ", msg
        socket.send(msg + '\r\n')

    recv = socket.recv(1024)
    print "<==Received:\n", recv
    if recv[:3]!=code:
        print '%s reply not received from server.' % code
    return recv

def send(socket, msg):
    print "Sending ==> ", msg
    socket.send(msg + '\r\n')

def main():
    # Some code from Downey some from my TCP server
    serverName       = 'smtp.cis.fiu.edu'
    serverPort       = 1994
    schoolServerPort = 25
    # Mail Server uses TCP so we need to open it
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Resuse address and go to socket layer
    tcpSocket.bind(('', serverPort)) # binds hostname with port
    serverSocket =  tcpSocket
    serverSocket.listen(1) # listening to one connections

    print("\nListening on port " + str(serverPort)) # str() - convert number to string

    print("Interrupt with CTRL-C")
    while True:
        try: ### try and catch for error handling ###
            # Establish the connection
            connectionSocket, address = serverSocket.accept() # accepts() = accept the connection and returns a socket
            message = connectionSocket.recv(4096) # recv() = receive the HTTP request
            print("\nHave established connection with IP address {0} and port {1}\n".format(address[0], address[1]))
            query = message.split()[1].partition("?")[2]

            # Given From Downey (Modified)
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            clientSocket.connect((serverName, schoolServerPort))
            recv = send_recv(clientSocket, None, '220')

            # parsin data function
            data = parsin(query)

            clientName = 'Cristina'
            userName = data['from'].split('@')[0]
            userServer = data['from'].split('@')[1]
            toName = data['to'].split('@')[0]
            toServer = data['to'].split('@')[1]
            subject = data['subject']
            message = data['message']

            #Given From Downey
            #Send HELO command and print server response.
            heloCommand = 'EHLO %s' % clientName
            recvFrom = send_recv(clientSocket, heloCommand, '250')
            #Send MAIL FROM command and print server response.
            fromCommand = 'MAIL FROM: <%s@%s>' % (userName, userServer)
            recvFrom = send_recv(clientSocket, fromCommand, '250')
            #Send RCPT TO command and print server response.
            rcptCommand = 'RCPT TO: <%s@%s>' % (toName, toServer)
            recvRcpt = send_recv(clientSocket, rcptCommand, '250')
            #Send DATA command and print server response.
            dataCommand = 'DATA'
            dataRcpt = send_recv(clientSocket, dataCommand, '354')

	    #Login to Mail Server
	    #username = "cvill141@fiu.edu"
	    #password = "Cevr20700922"
            authLoginRcpt = send_recv(clientSocket, "AUTH PLAIN LOGIN", '250')
	    #base64_str = ("\x00" + username + "\x00" + password).encode()	    
	    #base64_str = base64.b64encode(base64_str)
	    #authMsg = "AUTH LOGIN PLAIN".encode() + base64_str + "\r\n".encode()
	    #clientSocket.send(authMsg)
            
            print(authLoginRcpt)          
  
            #Send message data.
            send(clientSocket, "Date: %s" % time.strftime("%a, %d %b %Y %H:%M:%S -0400", time.localtime()));
            send(clientSocket, "From: %s@%s" % (userName, userServer));
            send(clientSocket, "Subject: %s" % subject);
            send(clientSocket, "To: %s@%s" % (toName, toServer));
            send(clientSocket, ""); #End of headers
            send(clientSocket, message)
            #Message ends with a single period.
            send_recv(clientSocket, ".", '250');
            #Send QUIT command and get server response.
            quitCommand = 'QUIT'
            quitRcpt = send_recv(clientSocket, quitCommand, '221')
        except KeyboardInterrupt:
                print("\n Interrupt by CTRL-C")
                break

if __name__ == '__main__':
    main()
