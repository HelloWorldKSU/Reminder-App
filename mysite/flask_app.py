
from flask import Flask, render_template, redirect, request
#import MySQLdb
from flask_sqlalchemy import SQLAlchemy
#import json

app = Flask(__name__)
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="zachbuchanan",
    password="enochroot",
    hostname="zachbuchanan.mysql.pythonanywhere-services.com",
    databasename="zachbuchanan$Reminders",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Tasks(db.Model):

    __tablename__ = "tasks"

    task_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'),
        nullable=False)
    task = db.Column(db.Text)

    def __init__(self, taskid_, userid_, task_):
        self.task_id = taskid_
        self.user_id = userid_
        self.task = task_

class Users(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(40))
    password = db.Column(db.String(255))
    email = db.Column(db.String(255))
    taskList = db.relationship('Tasks', backref='users', lazy=True)

#GETS: return type from gets is "Object Type" of Table.
#Ex: Selects on Task will return object
#of Task, with attributes such as Task.user_id, Task.task.
#tasks = Tasks.query.all()
#print(tasks[0].task)

#POSTS: Build new object type and add to db. Ex:
#rec = Tasks(2, 1, "learn something new")
#db.session.add(rec)
#db.session.commit()

@app.route('/')
def hello_world():
    tasks = Tasks.query.all()
    return render_template('index.html', tasks = tasks )

@app.route('/createItem', methods = ['POST'])
def create_item():
    newTask = request.form['reminder']
    newRec = Tasks(None, 1, newTask)
    db.session.add(newRec)
    db.session.commit()
    return redirect('/')
