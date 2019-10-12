
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#THIS IS FOR THE NOTE_APP DB
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="helloworldksu",
    password="cryptonomicon",
    hostname="helloworldksu.mysql.pythonanywhere-services.com",
    databasename="helloworldksu$note_app",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
#END NOTE_APP DB SETUP


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True) #NOT NEEDED??
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, username_, password_, email_):
        self.user_id = None
        self.username = username_
        self.password = password_
        self.email = email_

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

if __name__ == "__main__":
    app.run()
