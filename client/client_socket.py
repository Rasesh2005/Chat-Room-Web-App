from socket import socket , AF_INET, SOCK_STREAM, gethostbyname,gethostname
from threading import Thread

class ClientSocket:
    def __init__(self,username):
        self.CLIENT=socket(AF_INET,SOCK_STREAM)
        self.IP=gethostbyname(gethostname())
        self.PORT=1234
        self.ADDR=(self.IP,self.PORT)
        self.BUFF_SIZE=32
        self.FORMAT='utf-8'
        self.MsgList=[]
        self.username=username
    def send(self,username,msg):
        message=(f"{(len(username)+3+len(msg)):<{self.BUFF_SIZE}}"+username+":=>"+msg)
        self.CLIENT.send(message.encode(self.FORMAT))
    def recv(self):
        while True:
            msglen=int(self.CLIENT.recv(self.BUFF_SIZE).decode(self.FORMAT))
            if msglen:
                s=self.CLIENT.recv(msglen).decode(self.FORMAT)
                username=s[:s.index(':=>')]
                message=s[s.index(':=>')+3:]
                self.MsgList.append({username:message})
    def connect(self):
        self.CLIENT.connect(self.ADDR)
        Thread(target=self.recv).start()

