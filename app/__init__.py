from flask import Flask
from flask_mysqldb import MySQL
from flask_login import LoginManager

#Initialize the app
app = Flask(__name__)

#Load the config file
app.config.from_pyfile('../config.py')

#Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

#Initialize MySQL
mysql = MySQL(app)


#Connect to DataBase

#Load the views
from app import views

#Close DB connection on shutdown
'''
@app.teardown_appcontext
def close_db(error):
    if cur:
        cur.close()
'''
