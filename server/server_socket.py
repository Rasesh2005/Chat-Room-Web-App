from socket import gethostbyname, gethostname,SHUT_WR, socket, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM
from threading import Thread
import sys


class ServerSocket:
    """
    A Class to represent Server Socket.
    """
    def __init__(self, port:int) -> None:
        # Creating an INET , STREAMing socket
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        # make the server reusable
        self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.IP = '' # if on linux or hosting platfor
        if sys.platform == "win32" or sys.platform == "darwin": # if on windows or macOS
            self.IP = gethostbyname(gethostname())
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.BUFF_SIZE = 32
        self.FORMAT = 'utf-8'
        self.clients = [] # list of clients connected to server at the moment
        self.startServer()

    def broadcast(self, msg:bytes)-> None:
        """
        message consists of first 32(self.BUFF_SIZE) characters containing length of the message and next part is the message
        """
        message = (f"{len(msg):<{self.BUFF_SIZE}}"+msg.decode(self.FORMAT,'ignore'))
        for client in self.clients: 
            try:
                client.send(message.encode(self.FORMAT, 'ignore')) # keep sending byte by byte 
            except Exception as e:
                print(f'[BROADCAST ERROR] {e}')

    def handleClient(self, conn:socket)-> None:
        """
        A function to be threaded for each client. 
        The function Receives a message from the respective client and broadcasts it to all the clients

        Parameter
        ---------
        conn : socket
            client socket representative at server side
        """
        print(f"[NEW CONNECTION]")
        try:
            while True:
                #receiving the length of message
                msglen = conn.recv(self.BUFF_SIZE).decode(self.FORMAT, 'ignore')
                if msglen: # if received something
                    try:
                        # receive rest of the message
                        msg = conn.recv(int(msglen))
                        if msg:
                            self.broadcast(msg)
                    except Exception as e:
                        print(f'[HANDLECLIENT ERROR]{e}')
        except Exception as e:
            # Close the connection from erver side if client closes connection from client side
            print(f"[CONNECTION LOST] User: Connection Lost\n[EXCEPTION] {e}")
            conn.shutdown(SHUT_WR)
            conn.close()
            # remove client from clients list
            self.clients.remove(conn)

    def accept_connections(self):
        """
        A function to accept connections forever
        """
        while True:
            conn, addr = self.SERVER.accept()
            self.clients.append(conn)
            # making thread for each client and starting it
            client = Thread(target=self.handleClient, args=[conn])
            client.start()

    def startServer(self):
        self.SERVER.bind(self.ADDR)
        self.SERVER.listen()
        print(f"LISTENING FOR CONNECTIONS AT ({self.IP},{self.PORT})")
        # Make a thead to accept connections and return 
        Thread(target=self.accept_connections).start()
        # accepting conditions and other parts of program will occur simultaneously