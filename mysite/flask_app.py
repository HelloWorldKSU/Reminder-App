import os
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import LoginForm
from flask_login import current_user, login_user, UserMixin
from werkzeug.urls import url_parse


app = Flask(__name__)

#THIS IS FOR THE NOTE_APP DB
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="helloworldksu",
    password="cryptonomicon",
    hostname="helloworldksu.mysql.pythonanywhere-services.com",
    databasename="helloworldksu$note_app",
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

    user_id = db.Column(db.Integer, primary_key=True) #NOT NEEDED??
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))

    def __init__(self, username_, password_, email_):
        self.user_id = None
        self.username = username_
        self.password = password_
        self.email = email_

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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    #if current_user.is_authenticated:
    #    return redirect(url_for('index'))

    form = LoginForm()
    # true when the form is submitted, assuming all fields are valid
    if form.validate_on_submit():
        # returns user with username if it exists
        user = User.query.filter_by(username = form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            #flash('Invalid username or password')
            return redirect(url_for('login'))

        # from flask-login
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)

    return render_template('login_test.html', form = form)

if __name__ == "__main__":
    app.run()
