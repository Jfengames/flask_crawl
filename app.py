from flask import Flask,render_template,url_for
import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/login/')
def login():
    return render_template('login.html')


@app.route('/mission/')
def mission():
    return 'configure your crawler mission!'


if __name__ == '__main__':
    app.run(debug=True)
