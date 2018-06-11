from flask import Flask,render_template,url_for,request
from database import db,User
import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        return 'success'

    return render_template('login.html')


@app.route('/mission/')
@login_required
def mission():
    return 'configure your crawler mission!'


if __name__ == '__main__':
    app.run()

