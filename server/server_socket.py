from socket import socket ,SOL_SOCKET,SO_REUSEADDR, AF_INET, SOCK_STREAM, gethostbyname,gethostname
from threading import Thread
class ServerSocket:
    def __init__(self) -> None:
        #Creating an INET , STREAMing socket
        self.SERVER=socket(AF_INET,SOCK_STREAM)
        self.SERVER.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.IP=gethostbyname(gethostname())
        self.PORT=1234
        self.ADDR=(self.IP,self.PORT)
        self.BUFF_SIZE=32
        self.FORMAT='utf-8'
        self.clients=[]
        self.startServer()
    def broadcast(self,conn,msglen,msg):
        msg=(f"{msglen:<{self.BUFF_SIZE}}"+msg.decode(self.FORMAT)).encode(self.FORMAT)
        for client in self.clients:
            client.send(msg)
    def handleClient(self,conn):
        print(f"[NEW CONNECTION]")
        try:
            while True:
                msglen=int(conn.recv(self.BUFF_SIZE).decode(self.FORMAT))
                if msglen:
                    msg=conn.recv(msglen)
                    self.broadcast(conn,msglen,msg)
        except Exception as e:
            print(f"[CONNECTION LOST] User: Connection Lost")
            self.clients.remove(conn)
    def accept_connections(self):
        while True:
            conn,addr=self.SERVER.accept()
            self.clients.append(conn)
            client =Thread(target=self.handleClient, args=[conn])
            client.start()
    def startServer(self):
        self.SERVER.bind(self.ADDR)
        self.SERVER.listen(5)
        print(f"LISTENING FOR CONNECTIONS AT ({self.IP},{self.PORT})")
        Thread(target=self.accept_connections).start()