from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g,Blueprint,get_flashed_messages
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS
import config
from database import User,Adcode,Scenecode,ScrapeMissions,db
import pymysql



from toolbox import RegisterForm, LoginForm


user = Blueprint('user',__name__)

@user.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':

        login_form = LoginForm()

        return render_template('login.html', form=login_form)

    else:
        username = request.form.get('username')

        password = request.form.get('password')

        user = User.query.filter(User.username == username, User.password == password).first()

        if user:
            session['user_id'] = user.id

            session.permanent = True

            return redirect(url_for('index.home'))


        else:
            return u'邮箱或者密码错误！'



@user.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':

        register_form = RegisterForm()

        return render_template('register.html', form=register_form)

    else:
        register_form = RegisterForm()

        email = request.form.get('email')

        username = request.form.get('username')

        password1 = request.form.get('password')

        user = User.query.filter(User.email == email).first()

        if user:
            return u'该邮箱已经注册！'

        else:
            if register_form.validate_on_submit():

                user = User(email=email,username=username,password=password1)

                db.session.add(user)

                db.session.commit()

                # flash('注册成功')

                return redirect(url_for('user.login'))

            else:
                return u'参数错误'

@user.route('/logout/')
def logout():
    session.clear()

    return redirect(url_for('user.login'))


