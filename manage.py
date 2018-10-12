# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 15:44:20 2018

@author: X1Carbon
"""
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from main import app
from database import db


manager = Manager(app)

migrate = Migrate(app,db)

manager.add_command('db',MigrateCommand)

if __name__ == "__main__":
    manager.run()



