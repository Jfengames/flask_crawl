# conding=utf-8

from flask_sqlalchemy import SQLAlchemy, model
from datetime import datetime

from config import SQLALCHEMY_DATABASE_URI

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)

    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)


class Adcode(db.Model):
    __tablename__ = 'adcode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(50), nullable=False)
    adcode = db.Column(db.Integer, nullable=False)


class Scenecode(db.Model):
    __tablename__ = 'scenecode'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scene = db.Column(db.String(50), nullable=False)
    scenecode = db.Column(db.Integer, nullable=False)


class Scrape_Missions(db.Model):
    __tablename__ = 'scrape_missions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
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
    create_time = db.Column(db.DateTime, default=datetime.now)


if __name__ == '__main__':
    user_jh = User(mail='jiahuiwl@chinamobile.com', passwd='test')
    db.session.add(user_jh)
