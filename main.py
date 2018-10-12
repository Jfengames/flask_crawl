# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: Jfengames
"""

from flask import Flask,session
from database import db,User
import config
from apis.userapi import user
from apis.indexapi import index

app = Flask(__name__)
app.config.from_object(config)


db.init_app(app)
app.register_blueprint(blueprint=user)
app.register_blueprint(blueprint=index)


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()

        if user:
            return {'user':user}
    return {}

if __name__ == '__main__':
    app.run(debug=True)



