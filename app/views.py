from flask import render_template, redirect, jsonify
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User, Database, load_user
# from app.models import search_by_name, search_by_......
from . import mysql


@app.route('/')
def index():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'GET':
		return "signup form"
	else:
		#verify details
		data = request.get_json()
		if Database.addUser(data):
			return "User added successfully"
		else:
			return "Error"

@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	username = data['username']
	password = data['password']
	#verify user
	if Database.login(username, password):
		user = load_user(username)
		login_user(user)
		return redirect("/"+username)
	else:
		return "Incorrect credentials. Please try again.",401

@app.route("/getUser")
@login_required
def getUser():
	return current_user.username

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("/")

@app.route("/<username>")
@login_required
def home(username):
	data = Database.getUser(username)
	return jsonify(data[1])

	
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

@app.route("/search")
def search():
	return render_template('search.html')
	
@app.route("/search_by", methods=['POST'])
def search_by():
	method = request.json['method']
	text = request.json['text']
	print(method,text)
	'''
	if(method==" "):
		data = search_by_
	elif(method==" "):
		data = search_by_
		
	return data
	'''
	return "SEARCH DATA"

@app.route("/addproject", methods=['POST'])
@login_required
def addProject():
	if current_user.access == "admin":
		projDetails = request.get_json()
		#verify Data parameters
		if Database.addProject(data):
		#if successful
			return "Data saved successfully"
		else:
			return "Error saving data"
	return "Access denied" 

@app.route("/project/<project>", methods=['GET'])
def showProject(project):
	data = Database.getProject(project)
	if data is not False:
		return jsonify(data)
	else:
		return "Project not found"

@app.route('/check', methods=['POST'])
def checkbid():
	data = {'tender_id':5,'vender_id':6,'date':"c",'cost':10,'project_id':10}
	Database.addBid(data)
	return "asda"
