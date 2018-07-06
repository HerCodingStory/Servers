#TCPServer.py
from socket import socket, SOCK_STREAM, AF_INET, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR
import time
import os
# SOCK_STREAM = TCP
# AF_INET     = use IVP4

 # Fernando helped me with with accept-Language header parsing and reading

 # Parsin of the header has to be done by separating each value
def parsinLanguageHeader(languageHeader):
 	languages   = languageHeader.split(",")
     	localePairs = []

     	for language in languages:
 		if language.split(";")[0] == language:
 			localePairs.append((language.strip(), "1"))
 		else:
 			locale  =  language.split(";")[0].strip()
 			quality = language.split(";")[1].split("=")[1]
 			localePairs.append((locale, quality))

 	return localePairs;


def readFileLanguage(filename, languages):
 	for language in languages:
		languageFile = filename + "." + language[0]
		cwd = os.getcwd()
		languageFilePath = cwd + "/" + languageFile
		if os.path.isfile(languageFilePath):
			return languageFile

	return filename

def readFile(filename):
  	message = ""

     	with open(filename, 'r') as infile:
         	data = infile.read(4096) # read chunks of 4096 and return string

         	# while the file is not empty read file by chunks
         	while bool(data and data.strip()): # bool = converts to boolean
             		message += data
             		data = infile.read(4096)

     	infile.close()

 	return message

def sendFile(connectionSocket, filename, contentType, modifiedDate):
     	timestamp = os.path.getmtime(filename) # gets when the file was last modified
    	timestamp = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))

     	if bool(modifiedDate and modifiedDate.strip()) and modifiedDate >= timestamp:
         	print("\n304 File Not Modified")
         	print("\nLast Modified Date:  " + modifiedDate)

         	HeaderLine = "HTTP/1.1 " + '304' + " " + 'Not Modified' + "\r\nContent-Type: text/plain\r\n Content-Length: 0\r\n\r\n"
         	connectionSocket.send(HeaderLine.encode())
     	else:
 		print("200 - Everything is OK")

 		### sends the content of the file to the website ###
 		data   = readFile(filename) # gets data in file
 		# create a header that sends content of file to website
 		header = "HTTP/1.1 200 - Everything is OK\r\n"  + "Last-Modified: " + timestamp +  "\r\nContent-Type: " + contentType + "\r\nContent-Length: " + str(len(data)) + "\r\n\r\n"

 		# .send = encrypt into a byte string
 		connectionSocket.send((header + data).encode()) # encode = converts to bytes


def main():
 	filename            = ""
 	hostname            = ""
     	header              = ""
     	port                = 1994
     	numberOfConnections = 1

     	serverSocket = socket(AF_INET, SOCK_STREAM)
 	serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) # Resuse address and go to socket layer
     	serverSocket.bind((hostname, port)) # binds hostname with port
     	serverSocket.listen(numberOfConnections) # listening to possible connections

     	print("\nListening on port " + str(port)) # str() - convert number to string

     	print("Interrupt with CTRL-C")

     	while True:
 		try: ### try and catch for error handling ###
 		    	# Establish the connection

 			message = ""
 		   	print("Ready to Serve...\n")

 		    	connectionSocket, address = serverSocket.accept() # accepts() = accept the connection and returns a socket

 		    	### retrieve the HTTP request ###
 		    	while True:
 				data = connectionSocket.recv(4096).decode() # decode() = converts byte string to a string
 				# recv() = receive the HTTP request
 				message += data
 				if len(data) < 4096:
 			    		break

 		    	print(message)

 		    	filename = message.split()[1].partition("/")[2] # split() = split one string into two by "/"(partition)
 		    	modifiedDate = ''

 		    	headerList = message.split();
 		    	languageHeader = headerList[headerList.index("Accept-Language:") + 1] # gets whatever is after the Accept-language header
 		    	languages = parsinLanguageHeader(languageHeader) # function that parse the data

 		    	languageFilename = readFileLanguage(filename, languages)

 			if filename == languageFilename:
 		    		if 'If-Modified-Since:' in message:
 					modifiedDate = message.split('If-Modified-Since: ')[1]

 			cwd = os.getcwd()
     			filePath = cwd + "/" + languageFilename

     			if not os.path.isfile(filePath):
         			languageFilename = languageFilename + "." + languages[0]

 		    	sendFile(connectionSocket, languageFilename, "text/plain", modifiedDate)
 		    	# get it ready to shutdown the connection by not accepting more connections
 		    	connectionSocket.shutdown(SHUT_RDWR)
 		    	connectionSocket.close() # close the connection
 		except (IOError, OSError):
 		    	#### File not found error ###
 		    	print("404 - Not found " + filename + "\n")
 		    	# create a header that sends error to website
 		    	header = "HTTP/1.1 " + '404' + " " + 'Not Found' + "\r\nContent-Type: text/html\r\n Content-Length: 0\r\n\r\n"
 		    	# .send = encrypt into a byte string
 		    	htmlData = '''<!DOCTYPE html>
 					<html>
 				    		<head>
 							<meta charset="utf-8">
 							<title>You made a Mistake!!!</title>
 				   		</head>
 				    		<body>
 							<h1>404 - FILE NOT FOUND</h1>
 				    		</body>
 					</html>'''
 		    	connectionSocket.send((header + htmlData).encode()) # encode = converts to bytes
 		    	# get it ready to shutdown the connection by not accepting more connections
 		    	connectionSocket.shutdown(SHUT_RDWR)
 		    	connectionSocket.close()

 		except IndexError: ### Raised when a sequence subscript is out of range ###
 		    	print("400 - Bad Request\n")
 		   	# create a header that sends error to website
 		    	header = "HTTP/1.1 " + '400' + " " + 'Bad Request' + "\r\nContent-Type: text/plain\r\n Content-Length: 0\r\n\r\n"
 		    	# .send = encrypt into a byte string
 		    	connectionSocket.send(header.encode()) # encode = converts to bytes
 		    	# get it ready to shutdown the connection by not accepting more connections
 		    	connectionSocket.shutdown(SHUT_RDWR)
 		    	connectionSocket.close()

 		except KeyboardInterrupt: ### Stops the program ###
 		    	print("\nCTRL-C was pressed")
 		    	break

 	# get it ready to shutdown the connection by not accepting more connections
 	serverSocket.shutdown(SHUT_RDWR)
 	serverSocket.close() # close the connection

 # make sures to call main first
if __name__ == '__main__':
     main()
