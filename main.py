# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: X1Carbon
"""
import shutil
from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash
from config import HOST,DB,PASSWD,PORT,USER
import config
from database import User,Adcode,Scenecode,Scrape_Missions,db
from decorators import login_required
import json
import pymysql
import xlwt
import os
import time

from SpiderScheduler import SpiderScheduler

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
db.create_all(app=app)


sc = SpiderScheduler()

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
        conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
        cur = conn.cursor()
        sql="""
            select * from {} where city_adcode={}
            """.format('GaodeMapScene', adcode)
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
            adsl_server_auth=','.join(['adsl_proxy','changeProxyIp'])
        key=request.form.get('KEY')
        if key:
            pass
        else:
            key=','.join(['f628174cf3d63d9a3144590d81966cbd',
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
        dataoperation = Scrape_Missions(username=username, email=email, city=city, city_adcode=adcode, scene=scene,
                                        type_code=scenecode, adsl_server_url=adsl_server_url,
                                        adsl_auth=adsl_server_auth, keys=key,
                                        status='not start yet')

        db.session.add(dataoperation)
        db.session.commit()

        sc.update(dataoperation)

        return render_template("crawl.html", username=username, email=email, city=city, adcode=adcode, scene=scene, scenecode=scenecode)

@app.route('/something/')
@login_required
def something():
    # log=''
    # with open("C:/Users/X1Carbon/MapCrawler_test/MapCrawler/MapCrawler/110000.log", 'r',encoding='UTF-8') as f:
    #     for i in f:
    #         log += i
    #     return log
    return '后续修改'



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