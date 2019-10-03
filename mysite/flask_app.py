
from flask import Flask, render_template, redirect, request


app = Flask(__name__)
reminders = []

@app.route('/')
def hello_world():
    #return render_template('index.html', reminders = reminders )
    return render_template('index.html')


@app.route('/createItem', methods = ['POST'])
def createNote():
    note = request.form['reminder']
    reminders.append(note)
    return redirect('/returnIndex')

@app.route('/returnIndex')
def returnIndex():
    if(len(reminders)):
        return render_template('index.html', reminders = reminders)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run()
