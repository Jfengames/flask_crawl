# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: X1Carbon
"""
import shutil
from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User,Adcode,Scenecode
from exts import db
from decorators import login_required
import json
#from os import system

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

start_crawl_grid_file = 'start_grid.json'
config_online = 'config_online.py'

@app.route('/',methods=['GET','POST'])
def index():
    scene = request.form.get('scene')
#    print(scene)
    city = request.form.get('city')
#    print(city)
    _start = {}
    log=''
    with open(start_crawl_grid_file, 'w') as fh:
        #a = json.load(fh)
        scene = Scenecode.query.filter(Scenecode.scene == scene).first()
        if scene:
            _start['TYPES'] = str(scene.scenecode)
        _start['start_grid'] = "0"
        adcode = Adcode.query.filter(Adcode.city == city).first()
        if city:
            _start['CITY_ADCODE'] = str(adcode.adcode)
        _start['resolution'] = "0.01"
        fh.write(json.dumps(_start))
        fh.close()
    shutil.move("C:/Users/X1Carbon/flask_crawl/MapService/start_grid.json","C:/Users/X1Carbon/MapCrawler/MapCrawler/start_grid.json")
    
    with open(config_online,'w') as py:
        py.write("HOST = '36.155.125.243'\nPORT = 3306\nUSER = 'net_admin'\nPASSWD =  'Jtsdfg2018'\nDB = 'sdfg'\nCHARSET = 'utf8'\n")
        adsl_url = request.form.get('ADSL_SERVER_URL')
        py.write("ADSL_SERVER_URL = '"+str(adsl_url)+"'\n")
        adsl_auth = request.form.get('ADSL_SERVER_AUTH')
        py.write("ADSL_SERVER_AUTH = '"+str(adsl_auth)+"'")
        py.close()  
    shutil.move("C:/Users/X1Carbon/flask_crawl/MapService/config_online.py","C:/Users/X1Carbon/MapCrawler/MapCrawler/config.py")
    
    with open("C:/Users/X1Carbon/MapCrawler/MapCrawler/wulumuqi.log",'r') as f:    
        for i in f:
            log += i
#        print(log)
#    system("mv config_online.py ../destop/config_online.py")
    #print (app.config)    
    #print(Adcode.query.filter(Adcode.city=city).first())   
    
    return render_template("index.html",log=log)

@app.route('/something/')
@login_required
def something():
    a=''
    with open("C:/Users/X1Carbon/MapCrawler/MapCrawler/wulumuqi.log",'r') as f:
        
        #        
        for i in f:

            a += i
        return a


@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email,User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return u'邮箱或者密码错误！'
        

@app.route('/regist/',methods=['GET','POST'])
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
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))   

 
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()

        if user:
            return {'user':user}
    return {}
       
if __name__ == '__main__':
    app.run()