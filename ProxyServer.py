import socket
import threading

# Jose Helped me with multiThreading
class Server:
  config = # python dictionary
  { 
    "PROHIBIT_DOMAINS": ["youtube.com", "bing.com"]
  }
  
  #this method is used as a constructor for this class
  def __init__(self, hostname, portNumber):
    # Modified from TCP Server 
    self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a new socket using the address, type and protocol nomber
    self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)) # Resuse address and go to socket layer
    self.serverSocket.bind((hostname, portNumber)) # binds hostname with port
    self.serverSocket.listen(5) # listening to possible connections
    print("\nListening on port " + str(portNumber)) # str() - convert number to string
 	  print("Interrupt with CTRL-C")
    
  # Modified from TCP server
  # prepares server to shutdown
  def shutdownConnection(self):
    #before shutting down we have to stop all the threads
    mainThread = threading.current_Thread() #returns current thread object
    for thread in threading.enumerate(): # .enumerate = return a list of theads alive
      #This closes the main thread after all of the threads have finished. 
      if thread is mainThread:
        continue
      thread.joint() # wait until the thread terminates
    
    print("Shutting down proxy server.\n")
    self.serverSocket.shutdown(socket.SHUT_RDWR)
    self.serverSocket.close()
    
  # modified from TCP server
  #this method accepts the connection and creates and starts the threads
  def listenClient(self):
    while True:
      try:
        print("Waiting for a client\n")
        (connectionSocket, address) = self.serverSocket.accept() # Accept connection. The return value is a pair
        print("Connection established with IP address {0} and port {1}\n".format(address[0], address[1]))
        
        # this is calling the construtor in the class thread
        thread = threading.Thread(name=socket.gethostname(), # thread name
                                 target=self.proxyThreads, # runs the method proxy_thread
                                 args=(connectionSocket, address)) # contains an argument tuple which is going to be use for the target
        thread.setDaemon(True) # thread ends when main thread ends
        thread.start() #start the thread's activit
      except KeyboardInterrupt: # break program when Ctrl + C is pressed
        break
        
  def proxyThreads(self, connectionSocket, address):
    request = connectionSocket.recv(4096).decode() # receive request and decodes it
    firstLine = request.split('\r\n')[0] # splitting the request by new lines
    url = firstLine.split(' ')[1] # get the element in position 1. It should be the url
    
    if prohibitDomains(url): # if true, the website is forbidden and print and error
      httpResponse = ("HTTP/1.1 403 Forbidden\r\nContent-Length = 0\r\nConnection: Closed\r\n\r\n").encode()
      connectionSocket.send(httpResponse) # send the response to the socket
      connectionSocket.close() # close the connection
      return
    #else get web server and port and process the client request
    webServer, portNumber = getWebServerAndPort(url)
    #process client request
    processClientRequest(connect, webServer, portNumber, request)
    #shutdown server
    connectionSocket.shutdown(socket.SHUT_RDWR)
    connectionSocket.close()
   
#Check if website is in the black list
def prohibitDomains(url):
  for i in range(0, len(Server.config['PROHIBIT_DOMAINS'])):
    if Server.config['PROHIBIT_DOMAINS'][i] in url:
            return True
    return False

#Modified from FTP
def processClientRequest(self, WebServer, portNumber, request):
  webServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  webServerSocket.settimeout(5) # Set a timeout on blocking socket operations.
  
  try:
    webServerSocket.connect((webServer, portNumber)) # connect to remote socket at address
    webServerSocket.sendall(request) # send all data to socket until done or error
    
    data = webServerSocket.recv(4096).decode()  # receive request and decodes it
    #send data to browser
    while len(data) < 4096:
      self.send(data.encode()) 
      data = webServerSocket.recv(4096).decode()
      
  except OSError:
    print("Error: couldn't connect.")
  except socket.error as message:
    print(message)
    webServerSocket.shutdown(socket.SHUT_RDWR)
    webServerSocket.close()
    
def getWebServerAndPort(url):    
  httpPosition = url.find("://")
  print(httpPosition)
  
  if httpPosition != -1:
    url = url[(httpPosition + 3):]
    
  print(url)
  portPosition = url.find(':')
  
  print(portPosition)
  
  webServerPosition = url.find("/")
  
  if webServerPosition == -1:
    webServerPosition = len(url)
    
  print(webServerPosition)
  
  webServer = url[:webServerPosition]
  port = 80
  
  if portPosition < webServerPosition and portPosition != -1:
    webServer = url[:portPosition]
    port = int((url[(portPosition + 1):])[:webServerPosition - portPosition - 1])
  
  print(webServer)
  print(port)
  
  return webServer, port
  
def main():
  portNumber = 1994
  serverName = ''
  proxyServer = Server(socket.gethostbyname(serverName),portNUmber); # Translate a host name to IPv4 address format.
  proxyServer.listenClient();
  proxyServer.shutdownConnection();

if __name__ == "__main__":
  main()

