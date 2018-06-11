import os

DEBUG = True

USERNAME = 'net_admin'
PASSWD = 'Jtsdfg2018'
HOST = '36.155.125.243'
PORT = '3306'
DB = 'sdfg'

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(USERNAME,PASSWD,HOST,PORT,DB)
SQLALCHEMY_TRACK_MODIFICATIONS = False

