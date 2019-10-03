
from flask import Flask, render_template, redirect, request


app = Flask(__name__)
reminders = []

@app.route('/')
def hello_world():
    return render_template('index.html', reminders = reminders )

@app.route('/createItem', methods = ['POST'])
def createNote():
    note = request.form['reminder']
    reminders.append(note)
    return redirect('/')
    
if __name__ == "__main__":
    app.run()
