#FTPClient.py
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR, SHUT_RDWR, timeout
from ast import literal_eval
import time


def updateHTMLContent(connectionSocket, content):
    webPage = """
    <!DOCTYPE html> <html lang="en">
    <head>
        <title>FTP Filesystem</title>
        <h2 class="text-center">Welcome to my FTP Server Filesystem</h2>
    </head>
    <body>
        <div class="container">
            <form class="form-horizontal" method="POST" action="http://ocelot.aul.fiu.edu:1994">
                <div class="form-group">
                    <label for="path" class="col-sm-2 control-label">Enter a filename or directory path</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" id="path" name="path" placeholder="Enter a file or directory path.">
                        </div>
                </div>
            </form>
            <pre>
                {0}
            </pre>
        </div>
    </body>
    </html>
    """.format(content)

    httpResponse = "HTTP/1.1 200 OK\r\nContent-Length: " + str(len(webPage)) + "\r\nContent-Type: text/html\r\n\r\n" + webPage
    connectionSocket.send(httpResponse.encode('ascii'))

#this function sends a command to either dowload a file or get directory
def sendCommandData(socket, command, serverName):
    #given from downey
    # Create port number using last 2 numbers that are sent by the server
    message = send(socket, "PASV") # enter passive mode
    print(message)
    start = message. find("(")
    end = message.find(")")
    tuple = message[start + 1:end].split(',')
    serverPort = (int(tuple[4]) << 8) + int(tuple[5])

    dataSocket = socket(AF_INET,SOCK_STREAM)
    dataSocket.connect((serverName, serverPort))

    message = send(socket, command)
    responseCode = message.split()[0]

    response = ''

    if responseCode == "550":
        response = "Incorrect input\n"
    else:
        response = ""

        while True:
            data = dataSocket.recv(4096).decode('ascii')
            response += data
            if len(data) < 4096:
                break

        message = socket.recv(2048).decode('ascii')
        print(message)

    dataSocket.shutdown(SHUT_RDWR)
    dataSocket.close()

    return response

# Given from Downey
def send(socket, message):
    print "===>sending: " + message
    socket.send((message + "\r\n").encode('ascii', 'ignore'))
    receiver = socket.recv(1024).decode('ascii')
    print "<===receive: " + receiver
    return receiver

def processClientRequest(clientSocket, connectionSocket, serverName):
    print ("Move one directory to another or download a file.\n")

    while True:
        try:
            message = ""

            while True:
                data = connectionSocket.recv(4096).decode('ascii')
                message += data
                if len(data) < 4096:
                    break

            request = message.split()[0]

            # if the request is a get, then the client is entering the website for the  first time.
            # Get the path of the root directory and send it back to the web page
            if request == "GET":
                rootDirectory = sendCommandData(clientSocket,"LIST",serverName)
                updateHTMLContent(connectionSocket, rootDirectory)
            else:
                tokens = message.split("\r\n\r\n")
                queryString = tokens[1]
                fields = queryString.split("&")
                target = (fields[0].split("="))[1]
                result = ''

                response = send(clientSocket, "CWD" + target)
                status = response.split()[0]

                if status != "550":
                    result = sendCommandData(clientSocket, "LIST", serverName)
                else:
                    result = sendDataCommand(clientSocket, "RETR " + target, serverName)

                updateHTMLContent(connectionSocket, result)

        except timeout:
            print("Timeout due to inactivity")
            HeaderLine = "HTTP/1.1" + "408 Request Timeout" + "\r\nContent-Length = 0\r\nConnection:Closed\r\n\r\n"
            connectionSocket.send(HeaderLine.encode('ascii'))
            connectionSocket.shutdown(SHUT_RDWR)
            connectionSocket.close()

def main():
    #modified from downey
    remoteFTPCommandPort = 21
    remoteFTPServerName  = 'ftp.hq.nasa.gov'
    localServerPort      = 1994

    # Given From Downey
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((remoteFTPServerName,remoteFTPCommandPort))

    # From TCP server
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', localServerPort))
    serverSocket.listen(1)

    print("\nListening on port " + str(localServerPort)) # str() - convert number to string
    print("Interrupt with CTRL-C")

    # connect to FTP
    message = clientSocket.recv(2048).decode('ascii')
    print(message)
    #modified from downey
    condition = True

    while condition:
        message = clientSocket.recv(2048).rstrip()
        accept = "220 FTP Server Ready"
        condition = message[-len(accept):] != accept

    # Login to the remote FTP server 'ftp.swfwmd.state.fl.us'
    # Modified from downey
    send(clientSocket, "USER " + "anonymous")
    send(clientSocket, "PASS " + "cvill141@fiu.edu")
    send(clientSocket, "TYPE " + "A")

    while True:
        try:
            print("\nEstablishing connection with client...")
            connectionSocket, address = serverSocket.accept()
            connectionSocket.settimeout(200)
            print("\nHave established connection with IP address {0} and port {1}\n".format(address[0], address[1]))

            #Process Client Request
            processClientRequest(clientSocket, connectionSocket, remoteFTPServerName)

        except KeyboardInterrupt:
            message = send(clientSocket, "QUIT")
            print(message)
            clientSocket.shutdown(SHUT_RDWR)
            clientSocket.close()
            break

    serverSocket.shutdown(SHUT_RDWR)
    serverSocket.close()

if __name__ == '__main__':
    main()
