import os
from flask import Flask, render_template, redirect, request, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from forms import LoginForm
from flask_login import current_user, login_user, UserMixin, LoginManager
import pymysql

#from werkzeug.urls import url_parse


app = Flask(__name__)
login = LoginManager(app)

#THIS IS FOR THE NOTE_APP DB
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}".format(
    username="root",
    password="",
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

class Note(db.Model):
    __tablename__ = "note"

    id = db.Column(db.Integer, primary_key=True)
    user_id  = db.Column(db.Integer)
    title = db.Column(db.String(50))
    date_due_d = db.Column(db.Date)
    date_due_t = db.Column(db.Time)
    date_created_d = db.Column(db.Date)
    date_created_t = db.Column(db.Time)
    date_modified_d = db.Column(db.Date)
    date_modified_t = db.Column(db.Time)
    content  = db.Column(db.String(1000))

    def __init__(self, username_, password_, email_):
        self.id = None
        self.username = username_
        self.password = password_
        self.email = email_
    
    @property
    def serialize(self):
       return {
           'id' : self.id,
           'user_id' : self.user_id,
           'title' : self.title,
           'content' : self.content
       }
    @property
    def serialize_many2many(self):
       return [item.serialize for item in self.many2many]

@app.route('/')
def serveIndexHtml():
    return render_template('index.html')

#CREATE NEW USER POST METHOD
@app.route('/createNewUser', methods=['POST'])
def route_createNewUser():
    username_ = request.form['username_text_box']
    email_ = request.form['email_text_box']
    password_ = request.form['password_text_box']
    newUserAccountRecord = User(username_, password_, email_)
    db.session.add(newUserAccountRecord)
    try:
        db.session.commit()
    except exc.SQLAlchemyError as e:
        db.session().rollback()
        return jsonify(success=False)
    return _login(username_, password_)

#LOGIN METHOD
@app.route('/login', methods = ['POST'])
def route_login():
    username = request.form.get("auth_username_text_box")
    password = request.form.get("auth_password_text_box")
    return _login(username, password)

#login
def _login(username, password):
    user = User.query.filter_by(username = username).first()
    if not user or user.password != password:
        return jsonify(success=False)
    return jsonify(
	    success=True,
		user_id=user.id
	)

#NOTE METHOD
@app.route('/note')
def route_note():
    user_id = request.args.get('user_id')
    note = Note.query.filter_by(user_id = user_id)
    return jsonify(
	    success=True,
		notes=[i.serialize for i in note.all()]
	)

if __name__ == "__main__":
    app.run(use_reloader=True)







# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))

# # routes
# @app.route('/')
# def serveIndexHtml():
#     return render_template('index.html')

# @app.route('/signup')
# def serveCreateUserHtml():
#     return render_template('create_user.html')

# @app.route('/getEmail', methods = ['POST'])
# def get_email():
#     return redirect('/')

# @app.route('/createNewUser', methods = ['POST'])
# def createNewUserAccount():
#     username_ = request.form['username_text_box']
#     email_ = request.form['email_text_box']
#     password_ = request.form['password_text_box']
#     newUserAccountRecord = User(username_, password_, email_)
#     db.session.add(newUserAccountRecord)
#     db.session.commit()
#     return redirect('/')

# @app.route('/login', methods = ['GET', 'POST'])
# def login():
#     #if current_user.is_authenticated:
#     #    return redirect(url_for('index'))

#     form = LoginForm()
#     # true when the form is submitted, assuming all fields are valid
#     if form.validate_on_submit():
#         # returns user with username if it exists
#         user = User.query.filter_by(username = form.username.data).first()

#         if user is None or not user.check_password(form.password.data):
#             #flash('Invalid username or password')
#             return redirect(url_for('login'))

#         # from flask-login
#         login_user(user, remember = form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)

#     return render_template('login_test.html', form = form)