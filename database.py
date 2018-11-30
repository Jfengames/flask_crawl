# conding=utf-8
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy, model
from datetime import datetime
from config import SQLALCHEMY_DATABASE_URI
from werkzeug.security import check_password_hash, generate_password_hash


db = SQLAlchemy()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
DBSession = sessionmaker(bind=engine)

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    email = db.Column(db.String(50), unique=True)

    username = db.Column(db.String(50), unique=True)

    password = db.Column(db.String(256))

    is_activate = db.Column(db.Boolean, default=False)

    is_delete = db.Column(db.Boolean, default=False)

    def model_to_dict(self):
        return {"id":self.id, "name":self.u_name, "email":self.u_email, "password":self.u_password}

    #flask自带加密编码
    def set_password(self, password):
        self.u_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.u_password, password)

    def check_permission(self, permission):
        return self.u_permission & permission == permission


#帖子
class Note(db.Model):
    __tablename__ = 'note'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.String(64), nullable=False)

    content = db.Column(db.Text, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now, index=True)

    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))


    author = db.relationship('User', backref=db.backref('notes'))


#评论
class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    content = db.Column(db.Text, nullable=False)

    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    create_time = db.Column(db.DateTime, default=datetime.now, index=True)


    note = db.relationship('Note', backref=db.backref('comments', order_by = id.desc()))

    author = db.relationship('User', backref=db.backref('comments'))



class Adcode(db.Model):
    __tablename__ = 'adcode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    province = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    adcode = db.Column(db.Integer, nullable=False)


class Scenecode(db.Model):
    __tablename__ = 'scenecode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scene = db.Column(db.String(50), nullable=False)
    scenecode = db.Column(db.String(50), nullable=False)



class ScrapeMissions(db.Model):
    __tablename__ = 'scrape_missions'

    id = db.Column(db.Integer, autoincrement=True)

    username = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(50), nullable=False)

    city = db.Column(db.String(50), nullable=False)

    city_adcode = db.Column(db.String(6), primary_key=True)

    scene = db.Column(db.String(50), nullable=False)

    type_code = db.Column(db.String(6), primary_key=True)

    resolution = db.Column(db.Float, default=0.02)

    status = db.Column(db.String(100), nullable=False)

    final_grid = db.Column(db.Integer, default=0)

    adsl_server_url = db.Column(db.String(100), nullable=False)

    adsl_auth = db.Column(db.String(100), nullable=False)

    keys = db.Column(db.Text, nullable=False)

    create_time = db.Column(db.DateTime, default=datetime.now,onupdate=datetime.now)


class GaodeMapScene(db.Model):
    __tablename__ = 'gaodemapscene'

    id = db.Column(db.String(20),primary_key=True)

    province = db.Column(db.String(50))

    city = db.Column(db.String(50))

    name = db.Column(db.String(50))

    city_adcode = db.Column(db.String(20))

    district = db.Column(db.String(50))

    address = db.Column(db.String(100))

    longtitude = db.Column(db.Float(scale=10))

    lat = db.Column(db.Float(scale=10))

    type = db.Column(db.String(100))

    typecode = db.Column(db.String(20))

    classify = db.Column(db.String(100))

    area = db.Column(db.Float(scale=10))

    shape = db.Column(db.Text)

    wgs_long = db.Column(db.Float(scale=10))

    wgs_lat = db.Column(db.Float(scale=10))

    wgs_shape = db.Column(db.Text)


class CommonParameters(db.Model):
    __tablename__ = 'commonparameters'
    dt = db.Column(db.String(50))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))
    cgi = db.Column(db.String(50), primary_key=True)
    tac = db.Column(db.Integer, default=0)
    chinesename = db.Column(db.String(200))
    covertype = db.Column(db.String(50))
    scenario = db.Column(db.String(50))
    vendor = db.Column(db.String(50))
    earfcn = db.Column(db.Integer, default=0)
    nettype = db.Column(db.String(50))
    pci = db.Column(db.Integer, default=0)
    iscore = db.Column(db.Boolean, default=False)
    gpslat = db.Column(db.Float(scale=10))
    gpslng = db.Column(db.Float(scale=10))
    bdlat = db.Column(db.Float(scale=10))
    bdlng = db.Column(db.Float(scale=10))
    angle = db.Column(db.Integer, default=0)
    height = db.Column(db.String(50))
    totaltilt = db.Column(db.Float(scale=10))
    iscounty  = db.Column(db.Boolean, default=False)
    isauto = db.Column(db.Boolean, default=False)
    flag = db.Column(db.Boolean, default=False)


class CommonParameters_tagged(db.Model):
    __tablename__ = 'commonparameters_tagged'
    dt = db.Column(db.String(50))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))
    cgi = db.Column(db.String(50), primary_key=True)
    tac = db.Column(db.Integer, default=0)
    chinesename = db.Column(db.String(200))
    covertype = db.Column(db.String(50))
    scenario = db.Column(db.String(50))
    vendor = db.Column(db.String(50))
    earfcn = db.Column(db.Integer, default=0)
    nettype = db.Column(db.String(50))
    pci = db.Column(db.Integer, default=0)
    iscore = db.Column(db.Boolean, default=False)
    gpslat = db.Column(db.Float(scale=10))
    gpslng = db.Column(db.Float(scale=10))
    bdlat = db.Column(db.Float(scale=10))
    bdlng = db.Column(db.Float(scale=10))
    angle = db.Column(db.Integer, default=0)
    height = db.Column(db.String(50))
    totaltilt = db.Column(db.Float(scale=10))
    iscounty  = db.Column(db.Boolean, default=False)
    isauto = db.Column(db.Boolean, default=False)
    flag = db.Column(db.Boolean, default=False)
    residential_flag = db.Column(db.String(50), default=False)
    hospital_flag = db.Column(db.String(50), default=False)
    beauty_spot_flag = db.Column(db.String(50), default=False)
    college_flag = db.Column(db.String(50), default=False)
    food_centre_flag = db.Column(db.String(50), default=False)
    subway_flag = db.Column(db.String(50), default=False)
    high_speed_flag = db.Column(db.String(50), default=False)
    high_speed_rail_flag = db.Column(db.String(50), default=False)
    viaduct_flag = db.Column(db.String(50), default=False)
    high_rise_flag = db.Column(db.String(50), default=False)


class Gaodemapscene_tagged(db.Model):
    __tablename__ = 'gaodemapscene_tagged'
    id = db.Column(db.String(20), primary_key=True)
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    name = db.Column(db.String(50))
    city_adcode = db.Column(db.String(20))
    district = db.Column(db.String(50))
    address = db.Column(db.String(100))
    longtitude = db.Column(db.Float(scale=10))
    lat = db.Column(db.Float(scale=10))
    type = db.Column(db.String(100))
    typecode = db.Column(db.String(20))
    classify = db.Column(db.String(100))
    area = db.Column(db.Float(scale=10))
    shape = db.Column(db.Text)
    wgs_long = db.Column(db.Float(scale=10))
    wgs_lat = db.Column(db.Float(scale=10))
    wgs_shape = db.Column(db.Text)
    cgi_1 = db.Column(db.String(50))
    chinesename_1 = db.Column(db.String(200))
    pci_1 = db.Column(db.Integer)
    cgi_2 = db.Column(db.String(50))
    chinesename_2 = db.Column(db.String(200))
    pci_2 = db.Column(db.Integer)
    cgi_3 = db.Column(db.String(50))
    chinesename_3 = db.Column(db.String(200))
    pci_3 = db.Column(db.Integer)
    cgi_4 = db.Column(db.String(50))
    chinesename_4 = db.Column(db.String(200))
    pci_4 = db.Column(db.Integer)
    cgi_5 = db.Column(db.String(50))
    chinesename_5 = db.Column(db.String(200))
    pci_5 = db.Column(db.Integer)
    cgi_6 = db.Column(db.String(50))
    chinesename_6 = db.Column(db.String(200))
    pci_6 = db.Column(db.Integer)
    cgi_7 = db.Column(db.String(50))
    chinesename_7 = db.Column(db.String(200))
    pci_7 = db.Column(db.Integer)
    cgi_8 = db.Column(db.String(50))
    chinesename_8 = db.Column(db.String(200))
    pci_8 = db.Column(db.Integer)
    cgi_9 = db.Column(db.String(50))
    chinesename_9 = db.Column(db.String(200))
    pci_9 = db.Column(db.Integer)
    cgi_10 = db.Column(db.String(50))
    chinesename_10 = db.Column(db.String(200))
    pci_10 = db.Column(db.Integer)
    cgi_11 = db.Column(db.String(50))
    chinesename_11 = db.Column(db.String(200))
    pci_11 = db.Column(db.Integer)
    cgi_12 = db.Column(db.String(50))
    chinesename_12 = db.Column(db.String(200))
    pci_12 = db.Column(db.Integer)
    cgi_13 = db.Column(db.String(50))
    chinesename_13 = db.Column(db.String(200))
    pci_13 = db.Column(db.Integer)
    cgi_14 = db.Column(db.String(50))
    chinesename_14 = db.Column(db.String(200))
    pci_14 = db.Column(db.Integer)
    cgi_15 = db.Column(db.String(50))
    chinesename_15 = db.Column(db.String(200))
    pci_15 = db.Column(db.Integer)
    cgi_16 = db.Column(db.String(50))
    chinesename_16 = db.Column(db.String(200))
    pci_16 = db.Column(db.Integer)
    cgi_17 = db.Column(db.String(50))
    chinesename_17 = db.Column(db.String(200))
    pci_17 = db.Column(db.Integer)
    cgi_18 = db.Column(db.String(50))
    chinesename_18 = db.Column(db.String(200))
    pci_18 = db.Column(db.Integer)
    cgi_19 = db.Column(db.String(50))
    chinesename_19 = db.Column(db.String(200))
    pci_19 = db.Column(db.Integer)
    cgi_20 = db.Column(db.String(50))
    chinesename_20 = db.Column(db.String(200))
    pci_20 = db.Column(db.Integer)
    cgi_21 = db.Column(db.String(50))
    chinesename_21 = db.Column(db.String(200))
    pci_21 = db.Column(db.Integer)
    cgi_22 = db.Column(db.String(50))
    chinesename_22 = db.Column(db.String(200))
    pci_22 = db.Column(db.Integer)
    cgi_23 = db.Column(db.String(50))
    chinesename_23 = db.Column(db.String(200))
    pci_23 = db.Column(db.Integer)
    cgi_24 = db.Column(db.String(50))
    chinesename_24 = db.Column(db.String(200))
    pci_24 = db.Column(db.Integer)
    cgi_25 = db.Column(db.String(50))
    chinesename_25 = db.Column(db.String(200))
    pci_25 = db.Column(db.Integer)
    cgi_26 = db.Column(db.String(50))
    chinesename_26 = db.Column(db.String(200))
    pci_26 = db.Column(db.Integer)
    cgi_27 = db.Column(db.String(50))
    chinesename_27 = db.Column(db.String(200))
    pci_27 = db.Column(db.Integer)
    cgi_28 = db.Column(db.String(50))
    chinesename_28 = db.Column(db.String(200))
    pci_28 = db.Column(db.Integer)
    cgi_29 = db.Column(db.String(50))
    chinesename_29 = db.Column(db.String(200))
    pci_29 = db.Column(db.Integer)
    cgi_30 = db.Column(db.String(50))
    chinesename_30 = db.Column(db.String(200))
    pci_30 = db.Column(db.Integer)
    cgi_31 = db.Column(db.String(50))
    chinesename_31 = db.Column(db.String(200))
    pci_31 = db.Column(db.Integer)
    cgi_32 = db.Column(db.String(50))
    chinesename_32 = db.Column(db.String(200))
    pci_32 = db.Column(db.Integer)
    cgi_33 = db.Column(db.String(50))
    chinesename_33 = db.Column(db.String(200))
    pci_33 = db.Column(db.Integer)
    cgi_34 = db.Column(db.String(50))
    chinesename_34 = db.Column(db.String(200))
    pci_34 = db.Column(db.Integer)
    cgi_35 = db.Column(db.String(50))
    chinesename_35 = db.Column(db.String(200))
    pci_35 = db.Column(db.Integer)
    cgi_36 = db.Column(db.String(50))
    chinesename_36 = db.Column(db.String(200))
    pci_36 = db.Column(db.Integer)
    cgi_37 = db.Column(db.String(50))
    chinesename_37 = db.Column(db.String(200))
    pci_37 = db.Column(db.Integer)
    cgi_38 = db.Column(db.String(50))
    chinesename_38 = db.Column(db.String(200))
    pci_38 = db.Column(db.Integer)
    cgi_39 = db.Column(db.String(50))
    chinesename_39 = db.Column(db.String(200))
    pci_39 = db.Column(db.Integer)
    cgi_40 = db.Column(db.String(50))
    chinesename_40 = db.Column(db.String(200))
    pci_40 = db.Column(db.Integer)
    cgi_41 = db.Column(db.String(50))
    chinesename_41 = db.Column(db.String(200))
    pci_41 = db.Column(db.Integer)
    cgi_42 = db.Column(db.String(50))
    chinesename_42 = db.Column(db.String(200))
    pci_42 = db.Column(db.Integer)
    cgi_43 = db.Column(db.String(50))
    chinesename_43 = db.Column(db.String(200))
    pci_43 = db.Column(db.Integer)
    cgi_44 = db.Column(db.String(50))
    chinesename_44 = db.Column(db.String(200))
    pci_44 = db.Column(db.Integer)
    cgi_45 = db.Column(db.String(50))
    chinesename_45 = db.Column(db.String(200))
    pci_45 = db.Column(db.Integer)
    cgi_46 = db.Column(db.String(50))
    chinesename_46 = db.Column(db.String(200))
    pci_46 = db.Column(db.Integer)
    cgi_47 = db.Column(db.String(50))
    chinesename_47 = db.Column(db.String(200))
    pci_47 = db.Column(db.Integer)
    cgi_48 = db.Column(db.String(50))
    chinesename_48 = db.Column(db.String(200))
    pci_48 = db.Column(db.Integer)
    cgi_49 = db.Column(db.String(50))
    chinesename_49 = db.Column(db.String(200))
    pci_49 = db.Column(db.Integer)
    cgi_50 = db.Column(db.String(50))
    chinesename_50 = db.Column(db.String(200))
    pci_50 = db.Column(db.Integer)
    cgi_51 = db.Column(db.String(50))
    chinesename_51 = db.Column(db.String(200))
    pci_51 = db.Column(db.Integer)
    cgi_52 = db.Column(db.String(50))
    chinesename_52 = db.Column(db.String(200))
    pci_52 = db.Column(db.Integer)
    cgi_53 = db.Column(db.String(50))
    chinesename_53 = db.Column(db.String(200))
    pci_53 = db.Column(db.Integer)
    cgi_54 = db.Column(db.String(50))
    chinesename_54 = db.Column(db.String(200))
    pci_54 = db.Column(db.Integer)
    cgi_55 = db.Column(db.String(50))
    chinesename_55 = db.Column(db.String(200))
    pci_55 = db.Column(db.Integer)
    cgi_56 = db.Column(db.String(50))
    chinesename_56 = db.Column(db.String(200))
    pci_56 = db.Column(db.Integer)
    cgi_57 = db.Column(db.String(50))
    chinesename_57 = db.Column(db.String(200))
    pci_57 = db.Column(db.Integer)
    cgi_58 = db.Column(db.String(50))
    chinesename_58 = db.Column(db.String(200))
    pci_58 = db.Column(db.Integer)
    cgi_59 = db.Column(db.String(50))
    chinesename_59 = db.Column(db.String(200))
    pci_59 = db.Column(db.Integer)
    cgi_60 = db.Column(db.String(50))
    chinesename_60 = db.Column(db.String(200))
    pci_60 = db.Column(db.Integer)
    cgi_61 = db.Column(db.String(50))
    chinesename_61 = db.Column(db.String(200))
    pci_61 = db.Column(db.Integer)
    cgi_62 = db.Column(db.String(50))
    chinesename_62 = db.Column(db.String(200))
    pci_62 = db.Column(db.Integer)
    cgi_63 = db.Column(db.String(50))
    chinesename_63 = db.Column(db.String(200))
    pci_63 = db.Column(db.Integer)
    cgi_64 = db.Column(db.String(50))
    chinesename_64 = db.Column(db.String(200))
    pci_64 = db.Column(db.Integer)
    cgi_65 = db.Column(db.String(50))
    chinesename_65 = db.Column(db.String(200))
    pci_65 = db.Column(db.Integer)
    cgi_66 = db.Column(db.String(50))
    chinesename_66 = db.Column(db.String(200))
    pci_66 = db.Column(db.Integer)
    cgi_67 = db.Column(db.String(50))
    chinesename_67 = db.Column(db.String(200))
    pci_67 = db.Column(db.Integer)
    cgi_68 = db.Column(db.String(50))
    chinesename_68 = db.Column(db.String(200))
    pci_68 = db.Column(db.Integer)
    cgi_69 = db.Column(db.String(50))
    chinesename_69 = db.Column(db.String(200))
    pci_69 = db.Column(db.Integer)
    cgi_70 = db.Column(db.String(50))
    chinesename_70 = db.Column(db.String(200))
    pci_70 = db.Column(db.Integer)
    cgi_71 = db.Column(db.String(50))
    chinesename_71 = db.Column(db.String(200))
    pci_71 = db.Column(db.Integer)
    cgi_72 = db.Column(db.String(50))
    chinesename_72 = db.Column(db.String(200))
    pci_72 = db.Column(db.Integer)
    cgi_73 = db.Column(db.String(50))
    chinesename_73 = db.Column(db.String(200))
    pci_73 = db.Column(db.Integer)
    cgi_74 = db.Column(db.String(50))
    chinesename_74 = db.Column(db.String(200))
    pci_74 = db.Column(db.Integer)
    cgi_75 = db.Column(db.String(50))
    chinesename_75 = db.Column(db.String(200))
    pci_75 = db.Column(db.Integer)
    cgi_76 = db.Column(db.String(50))
    chinesename_76 = db.Column(db.String(200))
    pci_76 = db.Column(db.Integer)
    cgi_77 = db.Column(db.String(50))
    chinesename_77 = db.Column(db.String(200))
    pci_77 = db.Column(db.Integer)
    cgi_78 = db.Column(db.String(50))
    chinesename_78 = db.Column(db.String(200))
    pci_78 = db.Column(db.Integer)
    cgi_79 = db.Column(db.String(50))
    chinesename_79 = db.Column(db.String(200))
    pci_79 = db.Column(db.Integer)


class CommonParameters_tagged_new(db.Model):
    __tablename__ = 'commonparameters_tagged_new'
    dt = db.Column(db.String(50))
    province = db.Column(db.String(50))
    city = db.Column(db.String(50))
    region = db.Column(db.String(50))
    cgi = db.Column(db.String(50), primary_key=True)
    tac = db.Column(db.Integer, default=0)
    chinesename = db.Column(db.String(200))
    covertype = db.Column(db.String(50))
    scenario = db.Column(db.String(50))
    vendor = db.Column(db.String(50))
    earfcn = db.Column(db.Integer, default=0)
    nettype = db.Column(db.String(50))
    pci = db.Column(db.Integer, default=0)
    iscore = db.Column(db.Boolean, default=False)
    gpslat = db.Column(db.Float(scale=10))
    gpslng = db.Column(db.Float(scale=10))
    bdlat = db.Column(db.Float(scale=10))
    bdlng = db.Column(db.Float(scale=10))
    angle = db.Column(db.Integer, default=0)
    height = db.Column(db.String(50))
    totaltilt = db.Column(db.Float(scale=10))
    iscounty  = db.Column(db.Boolean, default=False)
    isauto = db.Column(db.Boolean, default=False)
    flag = db.Column(db.Boolean, default=False)
    residential_flag = db.Column(db.String(50), default=False)
    hospital_flag = db.Column(db.String(50), default=False)
    beauty_spot_flag = db.Column(db.String(50), default=False)
    college_flag = db.Column(db.String(50), default=False)
    food_centre_flag = db.Column(db.String(50), default=False)
    subway_flag = db.Column(db.String(50), default=False)
    high_speed_flag = db.Column(db.String(50), default=False)
    high_speed_rail_flag = db.Column(db.String(50), default=False)
    viaduct_flag = db.Column(db.String(50), default=False)
    high_rise_flag = db.Column(db.String(50), default=False)


class Todos(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime, default=datetime.now, index=True)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('tasks'))
    status = db.Column(db.Boolean, default=False)
    todo_city = db.Column(db.String(50))