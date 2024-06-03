# Flask Project - Online Banking

from flask import Flask,render_template,request,session,make_response
from database import Connection

app = Flask(__name__)
app.secret_key = 'xyz'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    return render_template('/index.html')

@app.route('/userhome')
def userhome():
    yourpass = request.cookies.get('yourpass')
    return render_template('userhome.html', yourpass=yourpass)

@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html')

@app.route('/transaction')
def transaction():
    return render_template('transaction.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/funds')
def funds():
    return render_template('funds.html')

@app.route('/setting')
def setting():
    return render_template('setting.html')

@app.route('/createAccount',methods=['POST','GET'])
def createAccount():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = float(request.form['tamt'])


        cnn = Connection()
        if cnn.storeAccount(email,acno,amt) == True:
            msg = "Account Created Succesfully !!!"
        else:
            msg = "Account Creation Failed !!!"
        return render_template('usermessage.html',message=msg)



@app.route('/viewAccount',methods=['POST','GET'])
def viewAccount():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])

        cnn = Connection()
        balance = cnn.checkAccount(email,acno)
        if balance > 0:
            msg = "Balance in Your Account = "+ str(balance)
        else:
            msg = "Account number is incorrect !!"
        return render_template('usermessage.html',message=msg)

@app.route('/performTrans',methods=['POST','GET'])
def performTans():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = float(request.form['tamt'])
        type = request.form['type']

        cnn = Connection()
        if cnn.storeTrans(email,acno,amt,type):
            msg = "Transaction Successful !!"
        else:
            msg = "Transaction Failed !!"
        return render_template('usermessage.html',message=msg)


@app.route('/mobileRecharge',methods=['POST','GET'])
def mobileRecharge():
    if request.method=='POST':
        email = request.form['temail']
        acno = int(request.form['tacno'])
        amt = float(request.form['tamt'])
        type = request.form['type']


        cnn = Connection()
        if cnn.storeRecharge(email,acno,amt,type):
            msg = "Mobile Recharge Succesful !!!"
        else:
            msg = "Mobile Recharge Failed !!!"

        return render_template('usermessage.html',message=msg)


@app.route('/transferFund', methods=['POST', 'GET'])
def transferFund():
    if request.method == 'POST':
        email = request.form['temail']
        acno1 = int(request.form['tacno1'])
        acno2 = int(request.form['tacno2'])
        amt = float(request.form['tamt'])

        cnn = Connection()
        if cnn.storeFundTransfer(email, acno1, acno2, amt):
            msg = "Fund Transfer Successful !!"
        else:
            msg = "Fund Transfer Failed !!"

        return render_template('usermessage.html', message=msg)


@app.route('/changePassword', methods=['POST', 'GET'])
def changePassword():
    if request.method == 'POST':
        email = request.form['temail']
        oldp = request.form['toldp']
        newp1 = request.form['tnewp1']
        newp2 = request.form['tnewp2']

        cnn = Connection()
        if cnn.checkPassword(email, oldp) == False:
            msg = "Your password is incorrect !!"
        else:
            if newp1 != newp2:
                msg = "Passowrd not matched !!!"
            else:
                if cnn.updatePassword(email, oldp, newp1) == True:
                    msg = "Password Update Successful !!"
                else:
                    msg = "Password Update Failed !!"

        return render_template('usermessage.html', message=msg)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/signupUser', methods=['GET', 'POST'])
def signupUser():
    if request.method == 'POST':
        email = request.form['uemail']
        pass1 = request.form['upass1']
        pass2 = request.form['upass2']

        # store data into database
        cnn = Connection()
        if cnn.storeUser(email, pass1) == True:
            msg = "Signup Successful !!!"
        else:
            msg = "Signup Failed !!!"
        return render_template('message.html', message=msg)


@app.route('/loginUser', methods=['GET', 'POST'])
def loginUser():
    if request.method == 'POST':
        email = request.form['uemail']
        pass1 = request.form['upass']

        # check the email and pass in the database
        cnn = Connection()
        if cnn.checkUser(email, pass1) == True:
            # use session to store data into session - email
            session['youremail'] = email
            resp = make_response(render_template('userhome.html'))
            resp.set_cookie('yourpass', pass1, max_age=60 * 5)
            return resp
        else:
            msg = "Login Failed !!!"
            return render_template('message.html',message=msg)


if __name__ == "__main__":
    app.run(debug=True)

