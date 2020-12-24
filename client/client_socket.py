from socket import socket , AF_INET, SOCK_STREAM
from multiprocessing import Process
import os
class ClientSocket:
    def __init__(self,port,username):
        self.CLIENT=socket(AF_INET,SOCK_STREAM)
        self.IP=''
        self.PORT=port
        self.ADDR=(self.IP,self.PORT)
        self.BUFF_SIZE=32
        self.FORMAT='utf-8'
        self.MsgList=[]
        self.username=username
    def send(self,msg):
        message=(f"{(len(self.username)+3+len(msg)):<{self.BUFF_SIZE}}"+self.username+":=>"+msg)
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
        self.send(self.username+" joined The chat")
        Process(target=self.recv).start()

    def close_client(self):
        self.CLIENT.close()