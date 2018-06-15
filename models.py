# -*- coding: utf-8 -*-

from exts import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(50),nullable=False)

    username = db.Column(db.String(50),nullable=False)
    password = db.Column(db.String(100),nullable=False)
    
class Adcode(db.Model):
    __tablename__ = 'adcode'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    city = db.Column(db.String(50),nullable=False)
    adcode = db.Column(db.Integer,nullable=False)
    
class Scenecode(db.Model):
    __tablename__ = 'scenecode'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    scene = db.Column(db.String(50),nullable=False)
    scenecode = db.Column(db.Integer,nullable=False)