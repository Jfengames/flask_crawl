# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: X1Carbon
"""
import shutil
from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash
import config
from models import User,Adcode,Scenecode,Dataoperation
from exts import db
from decorators import login_required
import json
import pymysql
import xlwt
import os
import time

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

start_crawl_grid_file = 'start_grid.json'
config_online = 'config_online.py'

@app.route('/',methods=['GET','POST'])
@login_required
def index():
    if request.method == 'GET':
        u=(1,2,3,4,5,6,7,8,9,10,11)
        return render_template('index.html',u=u)
    else:
        scene = request.form.get('scene')
        # scenecode = int(Scenecode.query.filter(Scenecode.scene == scene).first().scenecode)
        city = request.form.get('city')

        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        conn = pymysql.connect(host='127.0.0.1', user='root', password='19900411', db='flaskr', charset='utf8')
        cur = conn.cursor()
        sql="""
            select * from {} where city_adcode={}
            """.format('gaodemapscene_test', adcode)
        cur.execute(sql)
        u = cur.fetchall()
        if len(u) < 10:
            return render_template('index.html', u=u, city=city, scene=scene)
        else:
            fields = cur.description
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)

            # 写上字段信息
            for field in range(0, len(fields)):
                sheet.write(0, field, fields[field][0])

            # 获取并写入数据段信息

            for row in range(1, len(u) + 1):
                for col in range(0, len(fields)):
                    sheet.write(row, col, u'%s' % u[row - 1][col])

            workbook.save(r'./readout.xls')

            conn.close()
            return render_template('index.html', u=u)


@app.route('/crawl/',methods=['GET', 'POST'])
@login_required
def crawl():

    if request.method == 'GET':
        return render_template('crawl.html')
    else:
        user = User.query.filter(User.id == session.get('user_id')).first()
        username = user.username
        email = user.email
        city = request.form.get('city') 
        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        scene = request.form.get('scene')
        scenecode = int(Scenecode.query.filter(Scenecode.scene == scene).first().scenecode)
        adsl_server_url = request.form.get('ADSL_SERVER_URL')
        if adsl_server_url:
            pass
        else:
            adsl_server_url='http://223.105.3.170:18888'
        adsl_server_auth = request.form.get('ADSL_SERVER_AUTH')
        if adsl_server_auth:
            pass
        else:
            adsl_server_auth=str(('adsl_proxy','changeProxyIp'))      
        key=request.form.get('KEY')
        if key:
            pass
        else:
            key=str(['f628174cf3d63d9a3144590d81966cbd',
            '6cb7b3226b79fb9643ea4a72678db2e0',
            '4565bb15cfb2ab3b5c8214c669361a39',
            '3847127c1073379835f87fb8c6e1c5c4',
            '4e5b51a0ded99bd48363c3b75513a9fa',
            'df59636dada982e67fd0b599bba7a41a',
            '2a9c2dfb77af7d7b976c79e182d8d997',
            'fdf44b4a0e0925eead65fd17f2ffca2c',
            '3b5d262ae5b34061492d2bbb0efc9b74',
            '45d67ce8463c9a05bf175d718ed25330',
            'b1135364d5666872c1433f8f07b9740f',
            '59c8fc9fc15e0668e8b3dc1e2d2624a0',
            '36e7680730f3cd7e195c14b377643f4e',
            '27fdea7e7243f726f8a9d657806e19c7',
            '5269848e5e9bb7e107b666d4e9e04401',
            'b5792ffc8804de4d4fa32f0629849141',
            '5269848e5e9bb7e107b666d4e9e04401',
            ])     
        dataoperation = Dataoperation(username=username,email=email,city=city,adcode=adcode,scene=scene,scenecode=scenecode,adsl_server_url=adsl_server_url,adsl_server_auth=adsl_server_auth,key=key)

        db.session.add(dataoperation)
        db.session.commit()

        _start={}

        with open(start_crawl_grid_file, 'w') as fh:

            _start['TYPES'] = str(scenecode)
            _start['start_grid'] = 0

            _start['CITY_ADCODE'] = "110101"
            #str(adcode)
            _start['resolution'] = 0.01
            fh.write(json.dumps(_start))
            fh.close()
        shutil.move("C:/Users/X1Carbon/flask_crawl/MapService/start_grid.json","C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/start_grid.json")
        
        with open(config_online,'w') as py:
            py.write("HOST = '127.0.0.1'\nPORT = 3306\nUSER = 'root'\nPASSWD =  '19900411'\nDB = 'flaskr'\nCHARSET = 'utf8'\n")
            
            py.write("ADSL_SERVER_URL = '"+adsl_server_url+"'\n")

            py.write("ADSL_SERVER_AUTH = "+adsl_server_auth+"\n")
            
            py.write("KEYS = "+key+"\n")
            py.write("MAIL_NOTIFY = True\n")
            py.write("if MAIL_NOTIFY:\n")
            py.write("      MAIL_CONFIG = {'fromaddr': '13910154640@139.com','to': ['13651272822@139.com'], 'passwd': 'Lteumts2018','server': 'smtp.139.com'}")
            py.close()  
        shutil.move("C:/Users/X1Carbon/flask_crawl/MapService/config_online.py","C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/config.py")
        
        with open("C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/settings.py",'a') as st:
            st.write("\nLOG_FILE = '"+str(adcode)+".log'")

        os.chdir("C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/")
        os.system("python debug_run.py")
        
        #with open("C:/Users/X1Carbon/MapCrawler/MapCrawler/wulumuqi.log",'r') as f:
        #with open("C:/Users/X1Carbon/MapCrawler/MapCrawler/"+str(adcode)+".log",'r') as f:
        #    for i in f:
        #        log += i
    #        print(log)
    #    system("mv config_online.py ../destop/config_online.py")
        #print (app.config)    
        #print(Adcode.query.filter(Adcode.city=city).first())   
        
        return render_template("crawl.html", username=username, email=email, city=city, adcode=adcode, scene=scene, scenecode=scenecode)

@app.route('/something/')
@login_required
def something():
    log=''
    with open("C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/110000.log", 'r',encoding='UTF-8') as f:
        for i in f:
            log += i
        return log




@app.route('/download/', methods=['GET'])
def download_file():
    directory =os.getcwd()

    filename="readout.xls"
    return send_from_directory(directory,filename,as_attachment=True)


@app.route('/login/', methods=['GET', 'POST'])
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
    app.run(debug=True)