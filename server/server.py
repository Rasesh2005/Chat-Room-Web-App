import socket
import threading

#Creating an INET , STREAMing socket
SERVER=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
IP=socket.gethostbyname(socket.gethostname())
PORT=1234
ADDR=(IP,PORT)
SERVER.bind(ADDR)

MSG_SIZE=32
FORMAT='utf-8'
clients=[]
def handleClient(conn,username):
    print(f"[NEW CONNECTION] {username}")
    try:
        while True:
            msglen=int(conn.recv(MSG_SIZE).decode(FORMAT))
            if msglen:
                msg=conn.recv(msglen)
                broadcast(conn,username,msglen,msg)
    except Exception as e:
        print(f"[CONNECTION LOST] User: {username} Connection Lost")
        clients.remove(conn)

def broadcast(conn,username,msglen,msg):
    msg=(f"{(len(username)+3+msglen):<{MSG_SIZE}}"+username+":=>"+msg.decode(FORMAT)).encode(FORMAT)
    for client in clients:
        if not client==conn:
            client.send(msg)

def startServer():
    SERVER.listen(5)
    print(f"LISTENING FOR CONNECTIONS AT ({IP},{PORT})")
    while True:
        conn,addr=SERVER.accept()
        clients.append(conn)
        username=conn.recv(32).decode(FORMAT)
        client = threading.Thread(target=handleClient, args=(conn,username))
        client.start()


if __name__ == "__main__":
    startServer()