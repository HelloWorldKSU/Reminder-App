
from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="helloworldksu",
    password="cryptonomicon",
    hostname="helloworldksu.mysql.pythonanywhere-services.com",
    databasename="helloworldksu$signups",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Emails(db.Model):

    __tablename__ = "emails"

    email_address = db.Column(db.String(255), primary_key=True)

    def __init__(self, email_address_):
        self.email_address = email_address_


@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/getEmail', methods = ['POST'])
def get_email():
    email_ = request.form['email_text_box']
    newDbEmailRecord = Emails(email_)
    db.session.add(newDbEmailRecord)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    app.run()
