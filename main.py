from flask import Flask,render_template,request

app=Flask(__name__)

@app.route('/',methods=['GET'])
def login(name="login"):
    s=""
    if request.method=="GET":
        s=f"SUCCESSFULL SUBMISSION, USERNAME={request.GET.get('username')}"
    return render_template('login.html',name=name,mystring=s)

if __name__ == "__main__":
    app.run(debug=True)