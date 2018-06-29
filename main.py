# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: X1Carbon
"""
import shutil
from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS
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

        return render_template('index.html')
    else:
        scene = request.form.get('scene')
        # scenecode = int(Scenecode.query.filter(Scenecode.scene == scene).first().scenecode)
        city = request.form.get('city')
        # return redirect(url_for('show'),scene=scene,city=city)
        # return show(scene,city)
        return redirect(url_for('show',scene=scene,city=city))


@app.route('/show/',methods=['GET','POST'])
@login_required
def show():
    city = request.args.get('city')
    scene = request.args.get('scene')
    adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
    type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
    while not type_code%10:
        type_code //= 10

    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql_limit="""
            select * from {} where city_adcode={} and typecode like '{}%'limit 20
            """.format('GaodeMapScene', adcode,type_code)
    cur.execute(sql_limit)
    scrape_res = cur.fetchall()
    conn.close()

    if len(scrape_res) < 10:
        return render_template('show.html', scrape_res=scrape_res, city=city, scene=scene)
    else:

        return render_template('show.html', scrape_res=scrape_res, city=city, scene=scene)




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
        global adcode
        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        scene = request.form.get('scene')
        global scenecode
        scenecode = int(Scenecode.query.filter(Scenecode.scene == scene).first().scenecode)
        adsl_server_url = request.form.get('ADSL_SERVER_URL')
        if not adsl_server_url:
            adsl_server_url='http://223.105.3.170:18888'

        adsl_server_auth = request.form.get('ADSL_SERVER_AUTH')
        if not adsl_server_auth:
            adsl_server_auth=','.join(['adsl_proxy','changeProxyIp'])

        key=request.form.get('KEY')
        if not key:
            key=','.join(KEYS)

        final_gird = request.form.get('final_grid')
        if not final_gird:
            final_gird = 0


        g.mission = Scrape_Missions(username=username, email=email, city=city, city_adcode=adcode, scene=scene,
                                        type_code=scenecode, adsl_server_url=adsl_server_url,
                                        adsl_auth=adsl_server_auth, keys=key,final_grid=final_gird,
                                        status='not start yet')

        # 判断是否有重复的任务
        g.exist_mission =  Scrape_Missions.query.filter_by(city_adcode=g.mission.city_adcode,type_code=g.mission.type_code).all()

        if g.exist_mission:
            return render_template("reconfirm.html",exist_mission=g.exist_mission,mission=g.mission)

        else:
            db.session.add(g.mission)
            db.session.commit()

            msg = sc.update(g.mission)


            return render_template("crawl.html", username=username, email=email, city=city, adcode=adcode,
                                   scene=scene, scenecode=scenecode,msg=msg)


@app.route('/reconfirm/',methods=['GET','POST'])
@login_required
def reconfirm():
    if request.method == 'GET':
        # 显示元原任务详情以及当前任务详情
        return render_template('reconfirm.html',exist_mission=g.exist_mission,mission=g.mission)
    else:
        conformed = request.form.get('conform')
        if conformed == 'yes':
            #重新调度 任务
            db.session.add(g.mission)
            db.session.commit()

            msg = sc.update(g.mission)

            return render_template("crawl.html", username=g.mission.username, email=g.mission.email,
                                   city=g.mission.city, adcode=g.mission.adcode,
                                   scene=g.mission.scene, scenecode=g.mission.scenecode,
                                   msg=g.mission.msg)
        else:
            return render_template('show.html',scene=g.mission.scene,city=g.mission.city)



@app.route('/download/', methods=['GET'])
@login_required
def download():

    city = request.args.get('city')
    scene = request.args.get('scene')
    adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
    type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
    while not type_code%10:
        type_code //= 10
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql="""
            select * from {} where city_adcode={} and typecode like '{}%'
            """.format('GaodeMapScene', adcode, type_code)
    cur.execute(sql)
    total_res = cur.fetchall()
    fields = cur.description
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    # 获取并写入数据段信息

    for row in range(1, len(total_res) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % total_res[row - 1][col])

    workbook.save(r'./readout.xls')
    conn.close()
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