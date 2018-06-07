# conding=utf-8

from flask_sqlalchemy import SQLAlchemy,model



db = SQLAlchemy()

class User(db.model):
    id = db.Column(db.Integer,primary_key=True)
    mail = db.Column(db.String(20),nullable=False,unique=True)
    passwd = db.Column(db.string(20),nullable=False)


