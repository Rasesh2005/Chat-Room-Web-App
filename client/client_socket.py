from socket import socket , AF_INET, SOCK_STREAM, gethostbyname,gethostname
from threading import Thread

class ClientSocket:
    def __init__(self,username):
        self.CLIENT=socket(AF_INET,SOCK_STREAM)
        self.IP=gethostbyname(gethostname())
        self.PORT=1234
        self.ADDR=(self.IP,self.PORT)
        self.MSG_SIZE=32
        self.FORMAT='utf-8'
        self.MsgList=[]
        self.username=username
    def send(self,message):
        while True:
            msg=(f"{(len(self.username)+3+len(message)):<{self.MSG_SIZE}}"+self.username+":=>"+msg.decode(self.FORMAT)).encode(self.FORMAT)
            self.CLIENT.send(msg)
    def recv(self):
        while True:
            msglen=int(self.CLIENT.recv(self.MSG_SIZE).decode(self.FORMAT))
            if msglen:
                message=self.CLIENT.recv(msglen).decode(self.FORMAT)
                self.MsgList.append(message)
                print(f"Message Received by Client {self.username} Message={message}")
    def connect(self):
        self.CLIENT.connect(self.ADDR)
        Thread(target=self.recv)

