import socket
from threading import Thread

CLIENT=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
CLIENT.setblocking(False)
IP=socket.gethostbyname(socket.gethostname())
PORT=1234
ADDR=(IP,PORT)
CLIENT.connect(ADDR)
FORMAT='utf-8'
HEADER=64
UHEADER=16

def recv():
    pass
def send(username,msg):
    pass
def start_client(username):
    CLIENT.connect(ADDR)
    Thread(target=recv).start()

if __name__ == "__main__":
    start_client()