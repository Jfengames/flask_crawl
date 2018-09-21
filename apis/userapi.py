import shutil
from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g,Blueprint
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS,TABLE_NAME
import config
from database import User,Adcode,Scenecode,Scrape_Missions,db
from flask_restful import Resource
import json
import pymysql

user = Blueprint('user',__name__)

@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index.home'))
        else:
            return u'邮箱或者密码错误！'


@user.route('/regist/', methods=['GET', 'POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.email == email).first()
        if user:
            return u'该邮箱已经注册！'
        else:
            if password1 != password2:
                return u'两次密码不相同！'
            else:
                user = User(email=email,username=username,password=password1)
                print(user)
                db.session.add(user)
                db.session.commit()

                # time.sleep(3)
                return redirect(url_for('user.login'))

@user.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('user.login'))