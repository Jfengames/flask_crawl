# -*- coding: utf-8 -*-
import os

DEBUG = False

SECRET_KEY = os.urandom(24)

HOST = '127.0.0.1'
PORT = 3306
USER = 'root'
PASSWD =  '19900411'
DB = 'flaskr'

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USER,PASSWD,
HOST,PORT,DB)
SQLALCHEMY_DATABASE_URI =DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS=False


#HOST = '36.155.125.243'
#PORT = 3306
#USER = 'net_admin'
#PASSWD =  'Jtsdfg2018'
#DB = 'sdfg'
#CHARSET = 'utf8'

ADSL_SERVER_URL = 'http://223.105.3.170:18888'
ADSL_SERVER_AUTH = ('adsl_proxy','changeProxyIp')

KEYS = ['f628174cf3d63d9a3144590d81966cbd',
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
        ]
