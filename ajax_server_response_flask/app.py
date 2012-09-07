#!/usr/bin/python
from flask import Flask,render_template,request
import time,pkg_resources
app = Flask(__name__)

@app.route('/')
def user_prompt():
    version=pkg_resources.get_distribution('flask').version
    # Show the form with the version of Flask
    return render_template('user_prompt.html',flask_version=version)

@app.route('/givename', methods=['POST'])
def returnTime():
    if request.method == 'POST':
        # POST name was received. Return name|timestamp
        return "%s|%d" % (request.form['name'],time.time())
    else:
        # Nothing shows up if the request method is not POST
        return ""

if __name__ == '__main__':
    app.debug = True
    app.run()
