from threading import main_thread
from flask import Flask, render_template, request, redirect, jsonify
from client.client_socket import ClientSocket
from server.server_socket import ServerSocket
import logging
import sys

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


open_port = get_open_port()
server = ServerSocket(open_port)
users = []
connsDict = {}
userKeys = {}


@app.route('/', methods=['GET', "POST"])
def login(name="login"):
    global userKeys, connsDict, users
    s = ""
    if request.method == 'POST':
        username = request.form.get('username')
        key = request.form.get('key')
        if len(username) and len(username) < 32:
            if username in users and username.isalnum:
                if userKeys[username] == key:
                    return redirect(f'/chat/{username}')
                else:
                    return render_template('login.html', name=name, mystring="username already taken.. and the key also doesnt match for login")
            clientSocket = ClientSocket(open_port, username)
            clientSocket.connect()
            users.append(username)
            connsDict[username] = clientSocket
            userKeys[username] = key
            return redirect(f'/chat/{username}')
        else:
            s = "length of username should be between 1 and 32 and only alphanumeric characters allowed"
    return render_template('login.html', name=name, mystring=s)


@app.route('/chat/<string:username>/', methods=['GET', "POST"])
def chat(username, name="chat"):
    if request.method == 'POST':
        msg = request.form.get('msg')
        connsDict[username].sendMsg(msg)
        # return jsonify({"success":True})
    return render_template('chatPage.html', name=name, messages=connsDict[username].MsgList, key=userKeys[username], username=username)


@app.route('/chat/<string:username>/chat_list/')
def getChatList(username):
    if username in connsDict:
        print(connsDict)
        return jsonify(connsDict.get(username).MsgList)


@app.route('/leave/<string:username>/<string:key>/', methods=["GET", "POST"])
def leave_room(username, key):
    global connsDict, userKeys, users
    if userKeys.get(username) == key:
        conn = connsDict.get(username)
        conn.sendMsg(username+" left the chat..")
        conn.close_client()
        connsDict.pop(username, None)
        userKeys.pop(username, None)
        return redirect('/')
    else:
        print("KEY IS", userKeys.get('username'), "You Gave: ", key)
        return "Key Not Valid"


if __name__ == "__main__":
    app.run(threaded=True)
