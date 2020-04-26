# tcp-server-client
## TCP Client-Server System: Assignment for CS176A - Computer Communication Networks

Server and client should be run on different machines or different directories on the same machine.

When started, the client requests a server name or IP address, a specified port, and a command.  The client then validates the server and port and tries to connect and transmit the command to the server.

### The general interaction between the client and server is as follows:

1. The server starts and waits for a connection to be established by the client. 
2. When a command is received, then the server will:
  * Issue the command to its system and store the output in a file.
  * Open the file, read its content to a buffer.
  * Write the buffer contents to the connection established by the client.
3. The client will receive the data from the socket and store it in a local file.
