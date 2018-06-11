from flask import Flask,render_template,url_for
from database import db,User
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.route('/login/')
def login():
    user1 = User(mail='jiahuiwl@chinamobile.com', passwd='test')
    db.session.add(user1)
    db.session.commit()
    return render_template('login.html')


@app.route('/mission/')
def mission():
    return 'configure your crawler mission!'


if __name__ == '__main__':
    app.run()

