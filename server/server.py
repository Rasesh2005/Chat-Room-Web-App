from socket import socket,AF_INET,SOCK_STREAM,gethostbyname,gethostname
from threading import Thread
import select

# GLOBAL CONSTANT
SERVER=socket(AF_INET,SOCK_STREAM)
IP=gethostbyname(gethostname())
PORT=1234
ADDR=(IP,PORT)
SERVER.bind(ADDR)
UHEADER=16
HEADER=64
FORMAT='utf-8'
ROOM_SIZE=25

# Global Variables
clients=[]
client_threads=[]

def handle_client():
    while True:
        un_head=SERVER.recv(UHEADER).decode(FORMAT)
        if un_head:
            un_len=int(un_head)
            username=SERVER.recv(un_len).decode(FORMAT)
            msg_head=SERVER.recv(HEADER).decode(FORMAT)
            if msg_head:
                msg_len=int(msg_head)
                msg=SERVER.recv(msg_len).decode(FORMAT)
                broadcast(username,msg)
def broadcast(uname,msg):
    client_list,_,err_list=select.select(clients,[],clients)
    for client in client_list:
        try:
            client.send(f'{len(uname):<{UHEADER}}{uname}{len(msg):<{HEADER}}{msg}'.encode(FORMAT))
        except Exception as e:
            print(f'[EXCEPTION] {e}')

def start_server():
    SERVER.listen(ROOM_SIZE)
    print(f'[LISTENING] listening for connections at {ADDR}')
    while True:
        conn,addr=SERVER.accept()
        print(f'[NEW CONNECTION] connected to client({IP},{PORT}), Adddress:{addr}')
        clients.append(conn)
        client_thread=Thread(target=handle_client)
        client_thread.start()
        client_threads.append(client_thread)
    for client,thread in zip(clients,client_threads):
        client.close()
        thread.join()
    SERVER.close()
if __name__=="__main__":
    start_server()