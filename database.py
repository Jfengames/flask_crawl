# conding=utf-8

from flask_sqlalchemy import SQLAlchemy,model

from config import SQLALCHEMY_DATABASE_URI


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    mail = db.Column(db.String(50),primary_key=True)
    passwd = db.Column(db.String(50),nullable=False)








if __name__ == '__main__':



    user_jh = User(mail='jiahuiwl@chinamobile.com',passwd='test')
    db.session.add(user_jh)





