from flask import Flask,render_template,request,redirect,jsonify
from client.client_socket import ClientSocket
from server.server_socket import ServerSocket
app=Flask(__name__)
users=[]
clients=[]

@app.route('/',methods=['GET',"POST"])
def login(name="login"):
    global client
    s=""
    if request.method=='POST':
        username=request.form.get('username')
        if len(username) and len(username)<32:
            if username in users:
                return render_template('login.html',name=name,mystring=f"Username {username} already exists..")
            client=ClientSocket(username)
            client.connect()
            return redirect(f'/chat/{username}')
        else:
            s="Empty Username or more than 32 character"
    return render_template('login.html',name=name,mystring=s)

@app.route('/chat/<string:username>',methods=['GET',"POST"])
def chat(username,name="chat"):
    if request.method=='POST':   
        msg=request.form.get('msg')
        client.send(username,msg)
    return render_template('chatPage.html',name=name,messages=client.MsgList,username=username)


if __name__ == "__main__":
    server=ServerSocket()
    app.run(debug=True,threaded=True)