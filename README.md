# Servers

1.  TCP Server

This Server can:

- After your server is running, this web server processes HTTP messages.
- Reads files and displays content.
- Displays 404 error page if file is nonexisten.
- Implements the conditional GET. The server is able to accept requests from existing HTTP clients, like Firefox and Chrome.
- Implements the accept-language header. (It basically reads whatever language you browser''s language is a returns the corresponding file to that language)

From Wikipedia:

> The Transmission Control Protocol (TCP) is one of the main protocols of the Internet protocol suite. It originated in the initial network implementation in which it complemented the Internet Protocol (IP). Therefore, the entire suite is commonly referred to as TCP/IP. TCP provides reliable, ordered, and error-checked delivery of a stream of octets (bytes) between applications running on hosts communicating via an IP network. Major internet applications such as the World Wide Web, email, remote administration, and file transfer rely on TCP.

2. UDP Server & Client

This server can:

- Allows the client to give up if no response has been reveived within 1 second.
- Includes information about how long each response took. This will be the RTT.

From Wikipedia:

> With User Datagram Protocol (UDP), computer applications can send messages, in this case referred to as datagrams, to other hosts on an Internet Protocol (IP) network. Prior communications are not required in order to set up communication channels or data paths. UDP uses a simple connectionless communication model with a minimum of protocol mechanism. UDP provides checksums for data integrity, and port numbers for addressing different functions at the source and destination of the datagram. It has no handshaking dialogues, and thus exposes the user's program to any unreliability of the underlying network; There is no guarantee of delivery, ordering, or duplicate protection. UDP is suitable for purposes where error checking and correction are either not necessary or are performed in the application; UDP avoids the overhead of such processing in the protocol stack. Time-sensitive applications often use UDP because dropping packets is preferable to waiting for packets delayed due to retransmission, which may not be an option in a real-time system.

3. FTP Client

This server can:

- Displays a page that contains the listing of the root index of the server.
- it has a text box for the user to enter the name of the file or directory from the current directory. Uses POST to pass the data to the server.
- If the name is for a file, then download it. If the name is for a directory, then redisplay the page with the new directory listing.

From Wikipedia:

> The File Transfer Protocol (FTP) is a standard network protocol used for the transfer of computer files between a client and server on a computer network. FTP is built on a client-server model architecture and uses separate control and data connections between the client and the server. FTP users may authenticate themselves with a clear-text sign-in protocol, normally in the form of a username and password, but can connect anonymously if the server is configured to allow it. The first FTP client applications were command-line programs developed before operating systems had graphical user interfaces, and are still shipped with most Windows, Unix, and Linux operating systems. Many FTP clients and automation utilities have since been developed for desktops, servers, mobile devices, and hardware, and FTP has been incorporated into productivity applications, such as web page editors.

4. Mail Client

This server can:

- Accepts input from the HTTP browser. (The form accepts the From and To addresses, along with the Subject and Message.)
- Send email when button is clicked.
- it can contact a mail server that requires authentication.

From Wikipedia:

> Simple Mail Transfer Protocol (SMTP) is an Internet standard for electronic mail (email) transmission. Although electronic mail servers and other mail transfer agents use SMTP to send and receive mail messages, user-level client mail applications typically use SMTP only for sending messages to a mail server for relaying. Although proprietary systems (such as Microsoft Exchange and IBM Notes) and webmail systems (such as Outlook.com, Gmail and Yahoo! Mail) use their own non-standard protocols to access mail box accounts on their own mail servers, all use SMTP when sending or receiving email from outside their own systems.

5. Proxy Server

This server is supposed to:

- The proxy will receive requests for URLs.
- For each URL that is requested, create a folder. Create subfolders for each path in the URL. Store the cached copy of the file in that folder.
- Send a request to the URL. If a 304 is returned, then send the cached copy of the file to the original client. If 200 is returned, cache the new copy and then send it to the client.
- Do not allow access to youtube and bing.

From Wikipedia:

> In computer networks, a proxy server is a server (a computer system or an application) that acts as an intermediary for requests from clients seeking resources from other servers. A client connects to the proxy server, requesting some service, such as a file, connection, web page, or other resource available from a different server and the proxy server evaluates the request as a way to simplify and control its complexity. Proxies were invented to add structure and encapsulation to distributed systems. Today, most proxies are web proxies, facilitating access to content on the World Wide Web, providing anonymity and may be used to bypass IP address blocking.

6. HTML Ajax File

- In the page, list several buttons with country code of several contries, like US, DE, ES. Choose the countries you want. Include at least three.
- Name a div element that will contain cities.
- When a button for a country is clicked, initiate an Ajax request that populates the box with several cities from that country. Choose at least three cities for each country.

7. Cookies Server

This server is supposed to: 

- It's a web server that handles cookies.
- The web server only has to display one, dynamic page. The page will display all the cookies that the browser sends to the server.
- The web server should write two cookies on each response. You get to determine the names and values of the cookies that your server sends.

Some Website Pictures:
![alt text](https://github.com/cristyevr94/Servers/blob/master/index.PNG)

![alt text](https://github.com/cristyevr94/Servers/blob/master/mail-client-test1.PNG)

![alt text](https://github.com/cristyevr94/Servers/blob/master/mail-client-test2.PNG)
