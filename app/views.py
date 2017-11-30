from flask import render_template, redirect, jsonify
from flask import request
from flask_login import login_user, logout_user, login_required, current_user
from app import app
from app.models import User, Database, load_user
import json
from . import mysql

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")

@app.route('/contactUs')
def contactUs():
	return render_template("contact_us.html")

@app.route('/about')
def about():
	return render_template("about_us.html")

@app.route('/signup',methods=['GET','POST'])
def signup():
	if request.method == 'GET':
		return render_template("register.html")
	else:
		#verify details
		data = request.get_json()
		print(data)
		if Database.addUser(data):
			return "User added successfully"
		else:
			return "Error",401

@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	username = data['username']
	password = data['password']
	#verify user
	if Database.login(username, password):
		user = load_user(username)
		login_user(user)
		return redirect("/user/"+username)
	else:
		return "Incorrect credentials. Please try again.",401

@app.route("/getUser")
@login_required
def getUser():
	return jsonify([current_user.username,current_user.access])

@app.route("/logout")
@login_required
def logout():
	logout_user()
	return redirect("/")

@app.route("/user/<username>")
@login_required
def home(username):
	data = Database.getUser(username)
	print(data)
	return jsonify(data[1:3])

	
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
	return render_template('search.html',method=request.args.get('method'),data=request.args.get('text'))
	
@app.route("/search_by", methods=['POST'])
def search_by():
	method = request.json['method']
	text = request.json['text']
	print(method,text)
	data = Database.search_by({'method':method, 'data':text})
	print(data)
	if len(data)==0:
	    return "No Entries found",401
	return data

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
'''
@app.route("/project/id/<id>", methods=['GET'])
def showProject(id):
	data = Database.getProject(project)
	if data is not False:
		return jsonify(data)
	else:
		return "Project not found"
'''

@app.route('/project/title/<pname>', methods=['GET'])
def disp_project(pname):
	#get project by project name
	data = list(Database.getProject(pname))
	updates=[]
	tenders=[]
	type = 'n'
	try:
		if (current_user.access == "admin"):
			if(data[-1]=='a'):#if allocated send updates and specify type
				updates = Database.getUpdate(pname)
				type='aa'
			else:#else send tenders and specify type
				type='aw'
				#tenders = Database.
				tenders = (list(Database.getTender(pname)))
				for i in range(len(tenders)):
					tenders[i]=list(tenders[i])
				tenders = tenders
				print(tenders)
		else:
			if(data[-1]=='a' and Database.pAllocTo(current_user.username,data[1])):
				#contractor can make updates
				type = 'ca'
			else:
				#contractor can make bid if date is open
				type = 'cw'
			#dont send data but send 'contractor' as type
	except:
		pass
	print(type)
	return render_template('proj_info.html', project = data, type= type,\
                updates=updates, tenders=tenders)
	
@app.route('/check', methods=['POST'])
def checkbid():
	data = {'tender_id':5,'vender_id':6,'date':"c",'cost':10,'project_id':10}
	Database.addBid(data)
	return "asda"

@app.route('/admin', methods=['GET'])
@login_required
def admin():
    if not (current_user.access == "admin"):
        return "Access Denied",401
    return render_template('admin.html',method=request.args.get('method'),data=request.args.get('text'))

@app.route('/load_proj_data', methods=['POST'])
def load_proj_data():
	status = request.json['status']
	data = Database.getAlloProject(status)	
	print((data))
	return jsonify(list(data))

@app.route('/contractor/<uname>', methods=['GET'])
@login_required
def contractor(uname):
    if current_user.access == "admin" or  current_user.username == uname:
        data = Database.getContractor(uname)
        if len(data)==0:
            return "User not found",404
        return render_template("contractor.html",data = json.dumps(data))
    return "Invalid access",401

@app.route('/getBid/<cname>')
@login_required
def getBid(cname):
    if current_user.access == "admin" or current_user.username == cname:
        data = Database.getBid(cname)
        if len(data) == 0:
            return jsonify([])
        return jsonify(data)
    return "Invalid access",401

@app.route('/makeUpdate',methods=['POST'])
@login_required
def makeUpdate():
    data = request.get_json()
    if Database.putUpdate(data):
        return "Data added successfully"
    return "error",404

@app.route('/getUpdate/<pname>')
@login_required
def getUpdate(pname):
    data = Database.getUpdate(pname)
    return jsonify(data)
    
@app.route('/makeBid',methods=['POST'])
@login_required
def makeBid():
    data = request.get_json()
    data['vender'] = current_user.username
    if Database.addBid(data):
        return "Data added successfully"
    return "error",404

