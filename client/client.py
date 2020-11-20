from socket import socket,AF_INET,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
import threading

# GLOBAL CONSTANTS
CLIENT=socket(AF_INET,SOCK_STREAM)
# CLIENT.setblocking(False)
IP=gethostbyname(gethostname())
PORT=1234
ADDR=(IP,PORT)
FORMAT='utf-8'
HEADER=64
UHEADER=16

# Global variables
lock=threading.Lock()
messages=[]

def recv():
    while True:
        un_head=CLIENT.recv(UHEADER).decode(FORMAT)
        if un_head:
            un_len=int(un_head)
            username=CLIENT.recv(un_len).decode(FORMAT)
            msg_head=CLIENT.recv(HEADER).decode(FORMAT)
            if msg_head:
                msg_len=int(msg_head)
                msg=CLIENT.recv(msg_len).decode(FORMAT)
                print(f'{username}:=> {msg}')
                messages.append({username:msg})
def send(username,msg):
    CLIENT.send(f'{len(username):<{UHEADER}}{username}{len(msg):<{HEADER}}{msg}'.encode(FORMAT))
    return
def start_client(username):
    CLIENT.connect(ADDR)
    Thread(target=recv).start()

if __name__ == "__main__":
    username=input("Enter Username: ")
    start_client(username)