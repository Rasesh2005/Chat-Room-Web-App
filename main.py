import threading
from flask import Flask,render_template,request,redirect
from client.client import messages, send, start_client
app=Flask(__name__)
users=[]
conns=[]
@app.route('/',methods=['GET',"POST"])
def login(name="login"):
    s=""
    if request.method=='POST':
        print(request)
        username=request.form.get('username')
        if len(username):
            if username in users:
                return render_template('login.html',name=name,mystring=f"Username {username} already exists..")
            start_client(username)
            return redirect(f'/chat/{username}')
        else:
            s="Empty Username"
    return render_template('login.html',name=name,mystring=s)

@app.route('/chat/<string:username>',methods=['GET',"POST"])
def chat(username,name="chat"):
    global messages
    if request.method=='POST':   
        msg=request.form.get('msg')
        send(username,msg)
    return render_template('chatPage.html',name=name,messages=messages,username=username)


if __name__ == "__main__":
    app.run(debug=True)