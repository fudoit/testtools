#import SocketServer
import socketserver
import sys

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        # print "{} wrote: %s".format(self.client_address[0]) %self.data
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        # just send back the same data, but upper-cased
        # self.request.sendall(self.data.upper())
        # just send back index.html
        file_object = open('index.html')
        try:
            file_context = file_object.read()
            self.request.sendall(file_context.encode('utf-8'))
        finally:
            file_object.close()

if __name__ == "__main__":
    HOST = "0.0.0.0"
    PORT = int(sys.argv[1])

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
    
    print ("Serving TCP on %s port %d ..." %(HOST, PORT))
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
