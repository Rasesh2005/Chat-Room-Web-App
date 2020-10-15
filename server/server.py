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

def handle_client(client):
    while True:
        try:
            un_head=client.recv(UHEADER).decode(FORMAT)
            if un_head:
                un_len=int(un_head)
                username=client.recv(un_len).decode(FORMAT)
                msg_head=client.recv(HEADER).decode(FORMAT)
                if msg_head:
                    msg_len=int(msg_head)
                    msg=client.recv(msg_len).decode(FORMAT)
                    if msg=="EXIT":
                        client.close()

                    print(f"MESSAGE:{msg}")
                    broadcast(username,msg)
        except Exception as e:
            print(e)
            client.close()
            clients.remove(client)
            print(f'[CLOSED] connection lost from client..')
            return
def broadcast(uname,msg):
    for client in clients:
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
        client_thread=Thread(target=handle_client,args=[conn])
        client_thread.start()
        client_threads.append(client_thread)
    for client,thread in zip(clients,client_threads):
        client.close()
        thread.join()
    SERVER.close()
if __name__=="__main__":
    start_server()