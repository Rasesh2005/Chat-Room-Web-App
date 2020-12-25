from socket import gethostbyname, gethostname,SHUT_WR, socket, SOL_SOCKET, SO_REUSEADDR, AF_INET, SOCK_STREAM
from threading import Thread
import sys


class ServerSocket:
    def __init__(self, port) -> None:
        # Creating an INET , STREAMing socket
        self.SERVER = socket(AF_INET, SOCK_STREAM)
        self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.IP = ''
        if sys.platform == "win32" or sys.platform == "darwin":
            self.IP = gethostbyname(gethostname())
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.BUFF_SIZE = 32
        self.FORMAT = 'utf-8'
        self.clients = []
        self.startServer()

    def broadcast(self, msg):
        message = (f"{len(msg):<{self.BUFF_SIZE}}"+msg.decode(self.FORMAT,'ignore'))
        for client in self.clients:
            client.send(message.encode(self.FORMAT, 'ignore'))

    def handleClient(self, conn):
        print(f"[NEW CONNECTION]")
        while True:
            try:
                msglen = conn.recv(self.BUFF_SIZE).decode(self.FORMAT, 'ignore')
                if msglen:
                    try:
                        msg = conn.recv(int(msglen))
                        self.broadcast(msg)
                    except Exception as e:
                        print(e)
            except Exception as e:
                print(f"[CONNECTION LOST] User: Connection Lost\n[EXCEPTION] {e}")
                conn.shutdown(SHUT_WR)
                conn.close()
                self.clients.remove(conn)

    def accept_connections(self):
        while True:
            conn, addr = self.SERVER.accept()
            self.clients.append(conn)
            client = Thread(target=self.handleClient, args=[conn])
            client.start()

    def startServer(self):
        self.SERVER.bind(self.ADDR)
        self.SERVER.listen()
        print(f"LISTENING FOR CONNECTIONS AT ({self.IP},{self.PORT})")
        Thread(target=self.accept_connections).start()
