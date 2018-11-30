
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo
from config import HOST, USER, PASSWD, DB, TABLE_NAME_INDEX, TABLE_NAME_ANALYSIS, ALLOWED_EXTENSIONS, DIRECTORY, \
    TABLE_NAME_ANALYSIS_GAODE, TABLE_NAME_ANALYSIS_Commonparameters
import xlwt
import os
import xlrd
import numpy as np
import matplotlib.path as mpath
import pymysql
from shapely.geometry import Polygon
import matplotlib.patches as mpatches
import main
from database import Todos, db


def downloadcsvindex(city,scene):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
            select * from {} where city_adcode='{}' and typecode like '{}%'
            """.format(TABLE_NAME_INDEX,city,remove_zero(scene))
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
    workbook.save(r'./downlaodcsvindex.xls')
    conn.close()


def downloadcsvanalysis(city):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
            select * from {} where city='{}'
            """.format(TABLE_NAME_ANALYSIS,city)
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
    workbook.save(r'./downloadcsvanalysis.xls')
    conn.close()


def downloadcsvanalysis_gaode(city):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
                select * from {} where city='{}'
                """.format(TABLE_NAME_ANALYSIS_GAODE, city)
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
    workbook.save(r'./downloadcsvanalysis_gaode.xls')
    conn.close()


def remove_zero(input):
    b = str(input)[::-1]
    b = str(int(b))
    output = b[::-1]
    return output


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(filename):
    # table_name = filename.replace('.xls','')
    book = xlrd.open_workbook(str(os.path.join(DIRECTORY, filename)))
    sheet = book.sheets()[0]
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = conn.cursor()
#     query_create_tabel = """CREATE TABLE {} (
#   dt varchar(50) NULL DEFAULT NULL,
#   province varchar(50) NULL DEFAULT NULL,
#   city varchar(50) NULL DEFAULT NULL,
#   region varchar(50) NULL DEFAULT NULL,
#   cgi varchar(50) NOT NULL,
#   tac int(11) NULL DEFAULT NULL,
#   chinesename varchar(200) DEFAULT NULL,
#   covertype varchar(50) DEFAULT NULL,
#   scenario varchar(50) DEFAULT NULL,
#   vendor varchar(50) DEFAULT NULL,
#   earfcn int(11) NULL DEFAULT NULL,
#   nettype varchar(50) NULL DEFAULT NULL,
#   pci int(11) NULL DEFAULT NULL,
#   iscore tinyint(1) NULL DEFAULT NULL,
#   gpslat float NULL DEFAULT NULL,
#   gpslng float NULL DEFAULT NULL,
#   bdlat float NULL DEFAULT NULL,
#   bdlng float NULL DEFAULT NULL,
#   angle int(11) NULL DEFAULT NULL,
#   height varchar(50) NULL DEFAULT NULL,
#   totaltilt float NULL DEFAULT NULL,
#   iscounty tinyint(1) NULL DEFAULT NULL,
#   isauto tinyint(1) NULL DEFAULT NULL,
#   flag tinyint(1) NULL DEFAULT NULL,
#   residential_flag varchar(50) NULL DEFAULT NULL,
#   hospital_flag varchar(50) NULL DEFAULT NULL,
#   beauty_spot_flag varchar(50) NULL DEFAULT NULL,
#   college_flag varchar(50) NULL DEFAULT NULL,
#   food_centre_flag varchar(50) NULL DEFAULT NULL,
#   subway_flag varchar(50) NULL DEFAULT NULL,
#   high_speed_flag varchar(50) NULL DEFAULT NULL,
#   `high_speed_rail_flag` varchar(50) NULL DEFAULT NULL,
#   `viaduct_flag` varchar(50) NULL DEFAULT NULL,
#   `high_rise_flag` varchar(50) NULL DEFAULT NULL,
#   PRIMARY KEY (`cgi`) USING BTREE
# ) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_bin ROW_FORMAT = Dynamic;""".format(table_name)
#     cursor.execute(query_create_tabel)

    query_insert_into = """INSERT INTO {} (dt,province,city,region,cgi,tac,chinesename,covertype,scenario,vendor,earfcn,nettype,pci,iscore,gpslat,gpslng,bdlat,bdlng,angle,height,totaltilt,iscounty,isauto,flag,residential_flag,hospital_flag,beauty_spot_flag,college_flag,food_centre_flag,subway_flag,high_speed_flag,high_speed_rail_flag,viaduct_flag,high_rise_flag)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(TABLE_NAME_ANALYSIS_Commonparameters)
    for r in range(1, sheet.nrows):
        dt = sheet.cell(r, 0).value
        province = sheet.cell(r, 1).value
        city = sheet.cell(r, 2).value
        region = sheet.cell(r,3).value
        cgi = sheet.cell(r, 4).value
        tac = int(sheet.cell(r, 5).value)
        chinesename = sheet.cell(r, 6).value
        covertype = sheet.cell(r, 7).value
        scenario = sheet.cell(r, 8).value
        vendor = sheet.cell(r, 9).value
        earfcn = int(sheet.cell(r, 10).value)
        nettype = sheet.cell(r, 11).value
        pci = int(sheet.cell(r, 12).value)
        iscore = sheet.cell(r, 13).value
        gpslat = float(sheet.cell(r, 14).value)
        gpslng = float(sheet.cell(r, 15).value)
        bdlat = float(sheet.cell(r, 16).value)
        bdlng = float(sheet.cell(r, 17).value)
        angle = int(sheet.cell(r, 18).value)
        height = sheet.cell(r, 19).value
        totaltilt = float(sheet.cell(r, 20).value)
        iscounty = bool(sheet.cell(r, 21).value)
        isauto = bool(sheet.cell(r, 22).value)
        flag = bool(sheet.cell(r, 23).value)
        residential_flag = 0
        hospital_flag = 0
        beauty_spot_flag = 0
        college_flag = 0
        food_centre_flag = 0
        subway_flag = 0
        high_speed_flag = 0
        high_speed_rail_flag = 0
        viaduct_flag = 0
        high_rise_flag = 0

        values = (dt,province,city,region,cgi,tac,chinesename,covertype,scenario,vendor,earfcn,nettype,pci,iscore,gpslat,gpslng,bdlat,bdlng,angle,height,totaltilt,iscounty,isauto,flag,residential_flag,hospital_flag,beauty_spot_flag,college_flag,food_centre_flag,subway_flag,high_speed_flag,high_speed_rail_flag,viaduct_flag,high_rise_flag)
        cursor.execute(query_insert_into, values)
    cursor.close()
    conn.commit()
    conn.close()

#小区与场景关联
def commonparameters(city):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """select * from {} where city= %s and residential_flag='0'""".format(TABLE_NAME_ANALYSIS_Commonparameters)
    values = (city)
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def gaodemapscene(district,city,typecode):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM {} WHERE district like %s and city LIKE %s and typecode LIKE %s and wgs_shape is not null""".format(TABLE_NAME_INDEX)
    values = (district+'%',city+'%',notzero(typecode)+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def analysis_new_mission_commonparameters_tagged_contains(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            point = (float(lines[l][15]), float(lines[l][14]))
            p = Path(shape_array)
            if p.contains_points([point]):
                query_commonparameters_tagged = """UPDATE {} set residential_flag='1' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters,cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


def analysis_new_mission_commonparameters_tagged_100(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            angle = float(lines[l][18])
            point = (float(lines[l][15]), float(lines[l][14]))
            Path(shape_array)
            try:
                a = mpatches.Wedge(point, 0.0009, angle - 65, angle + 65)._path.vertices
                a = Polygon(a).buffer(0)
                b = Polygon(shape_array)
                c = a.intersection(b)
                Polygon(c)
                overlap = 1
            except NotImplementedError as e:
                overlap = 0
            if overlap > 0:
                query_commonparameters_tagged = """UPDATE {} set residential_flag='2' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters, cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


def analysis_new_mission_commonparameters_tagged_100_200(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            angle = float(lines[l][18])
            point = (float(lines[l][15]), float(lines[l][14]))
            Path(shape_array)
            try:
                a = mpatches.Wedge(point, 0.0018, angle - 65, angle + 65, width=0.0009)._path.vertices
                a = Polygon(a).buffer(0)
                b = Polygon(shape_array)
                c = a.intersection(b)
                polygon = Polygon(c)
                f = polygon.area / b.area
            except NotImplementedError as e:
                f = 0
            if f > 0.5:
                query_commonparameters_tagged = """UPDATE {} set residential_flag='3' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters, cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


#场景与小区关联
def analysis_new_mission_gaodemapscene_tagged(city):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    shapes = gaodemapscene1(city, 120000)

    for s in range(0, len(shapes)):
        gaodemapscene_id = shapes[s][0]
        district = shapes[s][5]
        region = district.replace('区', '').replace('县', '').replace('市', '')
        lines = commonparameters1(city, region)
        Path = mpath.Path
        i = 0
        for l in range(0, len(lines)):
            shape = shapes[s][16]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            angle = float(lines[l][18])
            point = (float(lines[l][15]), float(lines[l][14]))
            p = Path(shape_array)
            cgi = lines[l][4]
            chinesename = lines[l][6]
            pci = lines[l][12]

            if p.contains_points([point]):
                i += 1
                if i == 80:
                    print('超出范围')
                    break
                cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))

            else:
                try:
                    a = mpatches.Wedge(point, 0.0009, angle - 65, angle + 65)._path.vertices
                    a = Polygon(a).buffer(0)
                    b = Polygon(shape_array)
                    c = a.intersection(b)
                    Polygon(c)
                    overlap = 1
                except NotImplementedError as e:
                    overlap = 0
                if overlap > 0:
                    i += 1
                    if i == 80:
                        print('超出范围')
                        break
                    cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))

                else:
                    try:
                        a = mpatches.Wedge(point, 0.0018, angle - 65, angle + 65, width=0.0009)._path.vertices
                        a = Polygon(a).buffer(0)
                        b = Polygon(shape_array)
                        c = a.intersection(b)
                        polygon = Polygon(c)
                        f = polygon.area / b.area
                    except NotImplementedError as e:
                        f = 0
                    if f > 0.5:
                        i += 1
                        if i == 80:
                            print('超出范围')
                            break
                        cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))
        print('%.2f%%' % (s / len(shapes) * 100))
    cursor.close()
    db.commit()
    db.close()


def commonparameters1(city,region):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """
    select * from {} where city= %s and region like %s and pci is not null and chinesename is not null""".format(TABLE_NAME_ANALYSIS_Commonparameters)
    values = (city,region+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def gaodemapscene1(city,typecode):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """
    select * from {} where city like %s and typecode like %s and wgs_shape is not null""".format(TABLE_NAME_INDEX)
    values = (city+'%',notzero(typecode)+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def query_gaodemapscene(cgi,chinesename,pci,gaodemapscene_id,i):
    cgi_i ='cgi_'+str(i)
    chinesename_j ='chinesename_'+str(i)
    pci_k ='pci_'+str(i)
    a_list = [cgi_i,chinesename_j,pci_k,cgi,chinesename,pci,gaodemapscene_id,TABLE_NAME_ANALYSIS_GAODE]
    sql = """update {0[7]} set {0[0]}= '{0[3]}',{0[1]}= '{0[4]}',{0[2]}= {0[5]} where id= '{0[6]}'""".format(a_list)
    return sql


def notzero(input):
    b=str(input)[::-1]
    b=str(int(b))
    output=int(b[::-1])
    return str(output)


class RegisterForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])

    password = PasswordField(u'密码', validators=[DataRequired()])

    password2 = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('password', '两次密码不一致')])

    email = StringField(u'工作邮箱', validators=[DataRequired()], )

    submit = SubmitField(u'立即注册')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])

    password = PasswordField(validators=[DataRequired()])

    submit = SubmitField(u'登录')


class CardForm(FlaskForm):
    title = StringField(validators=[DataRequired()])

    content = TextAreaField(validators=[DataRequired()])

    submit = SubmitField(u'立即发布')


class CommentForm(FlaskForm):
    content = StringField(validators=[DataRequired()])

    submit = SubmitField(u'发表评论')


def celery_task(city,_city,todo_id):
    todo = Todos.query.filter(Todos.id == todo_id).first()
    main.data_operation.delay(city,_city)
    # # todo.status = True
    # db.session.add(todo)
    # db.session.commit()