from flask_login import UserMixin
from . import login_manager, mysql
import json

class User(UserMixin):
    def __init__(self, username, access):
        self.username = username
        self.access = access
    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    cur = mysql.connection.cursor()
    cur.execute("Select username,vender from login where username='"+username+"'")
    data = cur.fetchone()
    try:
        return User(data[0],data[1])
    except:
        return []

class Database():
    def login(username,password):
        cur = mysql.connection.cursor()
        cur.execute("Select * from login where username='"+username+"' and password='"+password+"'")
        data = cur.fetchone()
        if data:
            return True
        else:
            return False

    def getUser(username):
        cur = mysql.connection.cursor()
        cur.execute("Select * from admin where username ='"+ username+"'")
        data = cur.fetchone()
        if cur.rowcount != 0:
            return data
        cur.execute("Select * from vender where username ='"+username+"'")
        data = cur.fetchone()
        if cur.rowcount != 0:
            return data
        return "No data found"

    def addUser(data):
        cur = mysql.connection.cursor()
        try:
            if data['type'] == 'admin':
                cur.execute("insert into admin(username,password) values('"+data['username']+"','"+data['password']+"')")
            else:
                cur.execute("insert into vender(firm, \
                    firm_url,username,password,user_fname,mobile_no, \
                    pan_no,tan_no,vat_no) values('"+data['firm']+"','"+data['firm_url']+\
                    "','"+data['username']+\
                    "','"+data['password']+"','"+data['user_fname']+\
                    "','"+data['mobile_no']+"','"+data['pan_no']+"','"+data['tan_no']+\
                    "','"+data['vat_no']+"')")
        except Exception as e:
            print(e)
            return False
        mysql.connection.commit()
        return True
    
    def addProject(data):
        cur = mysql.connection.cursor()
        try:
            cur.execute("insert into project(title, state, district, project_category, bid_start_date,\
                bid_end_date,project_desc,project_status) values('"+data['title']+"','"+data['state']+"','"+data['district']+\
                "','"+data['project_category']+"','"+data['bid_start_date']+"','"+data['bid_end_date']+"','"+data['project_desc']+"','w')")
            mysql.connection.commit()
        except Exception as e:
            print(e)
            return False
        return True

    def getProject(title):
        cur = mysql.connection.cursor()
        try:
            cur.execute("Select * from project where title = '"+title+"'")
            data = cur.fetchone()
            return data
        except Exception as e:
            print(e)
            return False
    def getAlloProject(status):
        cur = mysql.connection.cursor()
        try:
            cur.execute("Select * from project where project_status = '"+status+"'")
            data = cur.fetchall()
            return data
        except Exception as e:
            print(e)
            return False
    def addBid(data):
        cur = mysql.connection.cursor()
        cur.execute("insert into tender(est_amt,tender_pub_date,tender_last_date,tender_active) values("+str(data['est_amt'])+",\
                '"+data['tender_pub_date']+"','"+data['tender_last_date']+"','w')")
        mysql.connection.commit()
        cur.execute("select * from project where title = '"+data['project']+"'")
        pid = cur.fetchone()[1]
        cur.execute("select * from vender where username = '"+data['vender']+"'")
        uid = cur.fetchone()[0]
        cur.execute("select tender_id from tender where tender_id = (select max(tender_id) from tender)")
        tid = cur.fetchone()[0]
        print(tid)
        cur.execute("insert into bidding(vender_id,tender_id, \
            project_id) values('"+str(uid)+"','"+str(tid)+"','"+str(pid)+"')")
        mysql.connection.commit()
        return True

    def search_by(data):
        cur = mysql.connection.cursor()
        if data['method']=='project_category':
            cur.execute("select * from tender_category where tender_category_name='"+data['data']+"'")
            dept = cur.fetchone()
            if not dept:
                return []
            data['data'] = str(dept[0])
        cur.execute("select * from project where "+data['method']+"='"+data['data']+"'")
        data = cur.fetchall()
        if len(data)>0:
            data = list(data)
            for i in range(len(data)):
                data[i] = list(data[i])
                data[i][5] = data[i][5].strftime('%Y-%m-%d')
                data[i][6] = data[i][6].strftime('%Y-%m-%d')
            return json.dumps(data)
        else:
            return []
    
    def getContractor(uname):
        cur = mysql.connection.cursor()
        cur.execute("select * from vender where username = '"+uname+"'")
        data = cur.fetchone()
        return data
    
    def getBid(cname):
        result = []
        cur = mysql.connection.cursor()
    #Get All bids made by the user
        cur.execute("select * from bidding where vender_id in (select vender_id from vender where username = '"+cname+"')")
        data = cur.fetchall()
        for i,d in enumerate(data):
            temp=[]
            cur.execute("select title from project where project_id = '"+str(d[3])+"'")
            temp.append(cur.fetchone()[0])
            cur.execute("select est_amt,tender_pub_date,tender_active from tender where tender_id = '"+str(d[2])+"'")
            temp.extend(list(cur.fetchone()))
            result.append(temp)
            print(result)
        return result

    def pAllocTo(username,project_id):
        cur = mysql.connection.cursor()
        cur.execute("select * from bidding where project_id = "+str(project_id)+" and vender_id in (select vender_id from vender where username = '"+username+"')")
        data = cur.fetchone()
        if data != None:
            return True
        return False

    def getTender(pname):
        cur = mysql.connection.cursor()
        cur.execute("select * from tender where tender_id in (select tender_id from bidding where project_id in (select project_id from project where title = '"+pname+"'))")
        data = cur.fetchall()
        if data == None:
            return []
        return data

    def putUpdate(data):
        cur = mysql.connection.cursor()
        print(data)
        cur.execute("select * from project where title='"+data['project']+"'")
        result = cur.fetchone()
        if result is None:
            return False
        pid = result[1]
        cur.execute("insert into updates(project_id,date,percentage,delays) values("+str(pid)+",'"+data['date']+"',"+str(data['percentage'])+",'"+data['delays']+"')")
        mysql.connection.commit()
        return True

    def getUpdate(pname):
        cur = mysql.connection.cursor()
        cur.execute("select * from updates where project_id in (select project_id from project where title = '"+pname+"')")
        data = cur.fetchall()
        if data is None:
            return []
        return data

    def approveTender(data):
        cur = mysql.connection.cursor()
        cur.execute("select project_id from bidding where tender_id = "+str(data['tender_id']))
        proj = cur.fetchone()[0]
        print(data['tender_id'])
        cur.execute("update tender set tender_active = 'r' where tender_id in (select tender_id from bidding where project_id ='"+str(proj)+"')")
        cur.execute("update project set project_status = 'a' where project_id ="+str(proj))
        cur.execute("update tender set tender_active='a' where tender_id="+str(data['tender_id']))
        cur.connection.commit()

    
'''
    def search_by_state(data)
        cur = mysql.connection.cursor()
        cur.execute("select * from project where state='%s'",data)
        data = cur.fetchall()
        return data

    def search_by_district(data)
        cur = mysql.connection.cursor()
        cur.execute("Select * from project where district='%s'",data)
        data = cur.fetchall()
        return data
'''             
