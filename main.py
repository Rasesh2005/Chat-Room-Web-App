from flask import Flask,render_template,request,redirect
from client.client import messages, start_client
app=Flask(__name__)
@app.route('/')
def login(name="login",methods=['GET','POST']):
    s=""
    if request.method=="POST":
        username=request.form.get('username')
        if len(username):
            start_client()
            return redirect('/chat')
        else:
            s="Empty Username"
    return render_template('login.html',name=name,mystring=s)

@app.route('/chat',methods=['GET',"POST"])
def chat(name="chat"):
    if request.method=='POST':   
        msg=request.form.get('msg')
    return render_template('chatPage.html',name=name,messages=messages)


if __name__ == "__main__":
    app.run(debug=True)