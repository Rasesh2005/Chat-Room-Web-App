from socket import gethostbyname, SHUT_WR, gethostname, socket, AF_INET, SOCK_STREAM
import sys
from threading import Thread


class ClientSocket:
    def __init__(self, port, username):
        self.CLIENT = socket(AF_INET, SOCK_STREAM)
        self.IP = ''
        if sys.platform == "win32" or sys.platform == "darwin":
            self.IP = gethostbyname(gethostname())
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.BUFF_SIZE = 32
        self.FORMAT = 'utf-8'
        self.MsgList = []
        self.username = username

    def sendMsg(self, msg):
        try:
            message = (
                f"{(len(self.username)+3+len(msg)):<{self.BUFF_SIZE}}"+self.username+":=>"+msg)
            self.CLIENT.send(message.encode(self.FORMAT, 'ignore'))
        except:
            pass

    def recv(self):
        while True:
            try:
                msglen = self.CLIENT.recv(self.BUFF_SIZE).decode(self.FORMAT, 'ignore')
                if msglen:
                    s = self.CLIENT.recv(int(msglen)).decode(self.FORMAT, 'ignore')
                    username = s[:s.index(':=>')]
                    message = s[s.index(':=>')+3:]
                    if len(message):
                        self.MsgList.append({username: message})
            except Exception as e:
                print(f"[RECEIVE EXCEPTION] {e}")

    def connect(self):
        self.CLIENT.connect(self.ADDR)
        self.sendMsg(self.username+" joined The chat")
        Thread(target=self.recv).start()

    def close_client(self):
        self.CLIENT.shutdown(SHUT_WR)
        self.CLIENT.close()
