from threading import main_thread
from flask import Flask, render_template, request, redirect, jsonify
from client.client_socket import ClientSocket
from server.server_socket import ServerSocket
import logging
import sys
from argon2 import PasswordHasher

ph = PasswordHasher()

app = Flask(__name__)

# to log errors on heroku console for easier debug
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


def get_open_port():
    """
    Function to find open port which is not in use at the moment..
    We Find it by:
     * Giving it empty IP and PORT 0 so that i finds everything by itself
     * Use s.getsockname()[1] to get port which is occupied by current socket object
     * Close the socket by s.close()
     * return the port so that SERVER and CLIENT can connect on it
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


# Getting open Port
open_port = get_open_port()
server = ServerSocket(open_port)
# list of usernames to prevent duplicate usernames
users = []
# Dictionary of username to its respective client socket to access its socket later
connsDict = {}
# Dictionary of User to their passwordHash They enter while Login
userKeys = {}


@app.route('/', methods=['GET', "POST"])
def login(name="login"):
    global userKeys, connsDict, users
    s = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('pass')
        passwordHash = ph.hash(password)

        if len(username) and len(username) < 32:
            if username in users and username.isalnum:
                # if passwordHash matches then redirect to chat of that person
                if ph.verify(userKeys.get(username), password):
                    return redirect(f'/chat/{username}')
                else:
                    return render_template('login.html', name=name, mystring="username already taken.. and the password also doesn't match for login")
            clientSocket = ClientSocket(open_port, username)
            clientSocket.connect()
            users.append(username)
            connsDict[username] = clientSocket
            userKeys[username] = passwordHash
            return redirect(f'/chat/{username}')
        else:
            s = "length of username should be between 1 and 32 and only alphanumeric characters allowed"
    return render_template('login.html', name=name, mystring=s)


@app.route('/chat/<string:username>/', methods=['GET', "POST"])
def chat(username, name="chat"):
    if request.method == 'POST':
        msg = request.form.get('msg')
        # accessing client for a username ans sending message using it
        connsDict[username].sendMsg(msg)

    return render_template('chatPage.html', name=name, messages=connsDict[username].MsgList, passwordHash=userKeys[username], username=username)


@app.route('/chat/<string:username>/chat_list/')
def getChatList(username):
    if username in connsDict:
        # returning messages list without authentication as
        # it is single room for all and everyone can access the chats by joining the room
        return jsonify(connsDict.get(username).MsgList)


@app.route('/leave/<string:username>/', methods=["GET", "POST"])
def leave_room(username):
    global connsDict, userKeys, users
    passwordHash = request.form.get("passwordHash")
    if userKeys[username] == passwordHash:
        conn = connsDict.get(username)
        conn.sendMsg(username+" left the chat..")
        conn.close_client()
        users.remove(username)
        connsDict.pop(username, None)
        userKeys.pop(username, None)
        return redirect('/')
    else:
        return "Password didn't Match"


if __name__ == "__main__":
    app.run(threaded=True)
