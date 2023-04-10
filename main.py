from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
import pickle
import numpy as np

filename = 'model.pkl'
model = pickle.load(open(filename, 'rb'))


app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="sql.freedb.tech", user="freedb_arhanjitsingh", 
password="84Xq#qvzD%$u99y", database="freedb_mobilesoftware")

cursor=conn.cursor()

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def about():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('main.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute(""" SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}' """
                    .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')

    cursor.execute("""INSERT INTO `users` (`user_id`,`name`,`email`,`password`) VALUES 
    (NULL,'{}', '{}','{}')""".format(name,email,password))
    conn.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

# @app.route('/')
# def home():
# 	return render_template('login.html')


@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'POST':

        battery = int(request.form['battery'])
        blue = request.form.get('blue')
        clocks = int(request.form['clocks'])
        cp = request.form.get('cp')
        fc = request.form.get('fc')
        fbs = request.form.get('fbs')
        intm = int(request.form['intm'])
        mdep = int(request.form['mdep'])
        trestbps = int(request.form['trestbps'])
        ncore = int(request.form['ncore'])
        pc = int(request.form['pc'])
        px_h = int(request.form['px_h'])
        px_w = int(request.form['px_w']) 
        ramm = int(request.form['ramm'])
        sc_h = int(request.form['sc_h'])
        sc_w = int(request.form['sc_w'])
        
        chol = int(request.form['chol'])
          
        threeg = int(request.form['threeg'])
            
        restecg = int(request.form['restecg'])
        
        wifi = int(request.form['wifi'])
        
        
        data = np.array([[battery,blue,clocks,cp,fc,fbs,intm,mdep,trestbps,ncore,pc,px_h,px_w,ramm,sc_h,sc_w,chol,threeg,restecg,wifi]])
        my_prediction = model.predict(data)
        
        return render_template('result.html', prediction=my_prediction)



if __name__=="__main__":
    app.run(debug=True)

 