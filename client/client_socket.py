from socket import gethostbyname, SHUT_WR, gethostname, socket, AF_INET, SOCK_STREAM
import sys
from threading import Thread


class ClientSocket:
    """
    A Class to represent client socket
    """
    def __init__(self, port:int, username:str)->None:
        self.CLIENT = socket(AF_INET, SOCK_STREAM)
        self.IP = '' # if on linux or hosting platform
        if sys.platform == "win32" or sys.platform == "darwin": # if on windows or mac
            self.IP = gethostbyname(gethostname())
        self.PORT = port
        self.ADDR = (self.IP, self.PORT)
        self.BUFF_SIZE = 32
        self.FORMAT = 'utf-8'
        self.MsgList = [] # to store all messages received(by recv thread) 
        self.username = username
        self.clientWorking=True
    def sendMsg(self, msg:str)->None:
        try:
            message = (
                f"{(len(self.username)+3+len(msg)):<{self.BUFF_SIZE}}"+self.username+":=>"+msg)
            self.CLIENT.send(message.encode(self.FORMAT, 'ignore'))
        except:
            pass

    def recv(self):
        try:
            # run until we close the client from app.py using close_client function
            while self.clientWorking:
                    #receiving the length of message
                    msglen = self.CLIENT.recv(self.BUFF_SIZE).decode(self.FORMAT, 'ignore')
                    # ignore for ignoring unknown characters in utf-8 code
                    if msglen: # if received something
                        try:
                            # receive rest of the message
                            s = self.CLIENT.recv(int(msglen)).decode(self.FORMAT, 'ignore') 
                        except:
                            continue # just for security if any issue occurs
                        # the message will be in the for username=>message so slicing the username and message
                        username = s[:s.index(':=>')]
                        message = s[s.index(':=>')+3:]
                        if len(message): # if any message received
                            self.MsgList.append({username: message})
        except Exception as e:
            # sometimes theres a chance server closes cnnection but client keeps receiving, so kept this try excpt block
            print(f"[RECEIVE EXCEPTION] {e}")
            self.close_client()

    def connect(self):
        """
        A Function to connect to server socket
        """
        self.CLIENT.connect(self.ADDR)
        self.sendMsg(self.username+" joined The chat")
        Thread(target=self.recv).start()

    def close_client(self):
        self.clientWorking=False # to stop recv thread
        # shutting down client socket (standard code)
        self.CLIENT.shutdown(SHUT_WR)
        self.CLIENT.close()
