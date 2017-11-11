from flask import render_template, redirect
from flask import request
from flask_login import login_user, logout_user, login_required
from app import app
from app.models import User

from . import mysql
#sample user
user = User('admin','password')


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    #verify user
    cur = mysql.connection.cursor()
    cur.execute("Select * from login where username='"+username+"' and password='"+password+"'")
    data = cur.fetchone()
    if data:
        login_user(user)
        return redirect("/"+username)
    else:
        return abort(401)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route("/<username>")
@login_required
def home(username):
    return "Username: "+username

	
@app.route("/bids/<pname>")
def bids(pname):
	#fetch details of pname and send it in this json
	project = {'name':pname}
	return render_template('bid.html', project = project)
	
@app.route("/makebid/<pname>")
def makebid(pname):
	#get required details needed for the project and accordingly populate the form queries
	project = {'name':pname}
	return render_template('makebid.html', project = project)
	
@app.route("/bidplaced", methods=['POST'])
def bidplaced():
	return "A"