from flask_login import UserMixin
from . import login_manager, mysql

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.username

    def get_id(self):
        return self.username

@login_manager.user_loader
def load_user(username):
    cur = mysql.connection.cursor()
    cur.execute("Select username,password from login where username='"+username+"'")
    data = cur.fetchone()
    return User(data[0],data[1])
