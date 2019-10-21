import os
from flask import Flask, render_template, redirect, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_login import current_user, login_user, UserMixin, LoginManager
#from werkzeug.urls import url_parse


app = Flask(__name__)
login = LoginManager(app)

#THIS IS FOR THE NOTE_APP DB
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="root",
    hostname="localhost",
    databasename="reminder_app",
    # username="helloworldksu",
    # password="cryptonomicon",
    # hostname="helloworldksu.mysql.pythonanywhere-services.com",
    # databasename="helloworldksu$note_app",
)
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'you-will-never-guess')
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#END NOTE_APP DB SETUP

#db models
class User(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True) 
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, username_, password_, email_):
        self.id = None
        self.username = username_
        self.password = password_
        self.email = email_

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# routes
@app.route('/')
def serveIndexHtml():
    return render_template('index.html')

@app.route('/signup')
def serveCreateUserHtml():
    return render_template('create_user.html')

@app.route('/getEmail', methods = ['POST'])
def get_email():
    return redirect('/')

@app.route('/createNewUser', methods = ['POST'])
def createNewUserAccount():
    username_ = request.form['username_text_box']
    email_ = request.form['email_text_box']
    password_ = request.form['password_text_box']
    newUserAccountRecord = User(username_, password_, email_)
    db.session.add(newUserAccountRecord)
    db.session.commit()
    return redirect('/')

@app.route('/login_user')
def serveLoginTestHtml():
    return render_template('login_test.html')

@app.route('/login', methods = ['POST'])
def user_login():
    username = request.form.get("auth_username_text_box")
    password = request.form.get("auth_password_text_box")

    user = User.query.filter_by(username = username).first()

    if not user or user.password != password:
        flash("ERROR")
        return redirect('/login_user')

    return redirect('/')

if __name__ == "__main__":
    app.run()
