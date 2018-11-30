from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g,Blueprint
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS,TABLE_NAME_INDEX,DIRECTORY
from database import User,Adcode,Scenecode,ScrapeMissions,db,GaodeMapScene
from decorators import login_required
import pymysql
from sqlalchemy import and_
import xlwt
import os
from toolbox import remove_zero,downloadcsvindex

index = Blueprint('index',__name__)


@index.route('/',methods=['GET','POST'])
@login_required
def home():
    if request.method == 'GET':

        return render_template('index.html')
    else:
        city = request.form.get('city')
        scene = request.form.get('scene')
        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
        typecode = remove_zero(_typecode)

        gaodemapscene = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,GaodeMapScene.typecode.like(typecode+"%")).limit(1000).all()
        if gaodemapscene==[]:
            flash('请联系管理员获取你想要的数据！')
            return redirect(url_for('index.home'))
        else:
            downloadcsvindex(adcode,typecode)
            return render_template('index.html',gaodemapscene=gaodemapscene)


# @index.route('/show/',methods=['GET','POST'])
# @login_required
# def show():
#     city = request.args.get('city')
#     scene = request.args.get('scene')
#     adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
#     type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
#
#     type_code = remove_zero(type_code)
#
#     conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
#     cur = conn.cursor()
#     sql_limit="""
#             select * from {} where city_adcode={} and typecode like '{}%'limit 20
#         """.format(TABLE_NAME, adcode,type_code)
#     cur.execute(sql_limit)
#     scrape_res = cur.fetchall()
#
#     return render_template('show.html', scrape_res=scrape_res, city=city, scene=scene)

@index.route('/download/', methods=['GET'])
@login_required
def download1():
    filename = "downlaodcsvindex.xls"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)




#     city = request.args.get('city')
#     scene = request.args.get('scene')
#     adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
#     type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
#     type_code = remove_zero(type_code)
#     conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
#     cur = conn.cursor()
#     sql="""
#             select * from {} where city_adcode={} and typecode like '{}%'
#             """.format(TABLE_NAME, adcode, type_code)
#     cur.execute(sql)
#     total_res = cur.fetchall()
#     fields = cur.description
#     workbook = xlwt.Workbook()
#     sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
#
#     # 写上字段信息
#     for field in range(0, len(fields)):
#         sheet.write(0, field, fields[field][0])
#
#     # 获取并写入数据段信息
#
#     for row in range(1, len(total_res) + 1):
#         for col in range(0, len(fields)):
#             sheet.write(row, col, u'%s' % total_res[row - 1][col])
#
#     workbook.save(r'./readout.xls')
#     conn.close()
#     directory = os.getcwd()
#
#     filename = "readout.xls"
#     return send_from_directory(directory, filename, as_attachment=True)