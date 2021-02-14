#Imports
import firebase_admin
import pyrebase
import json
from src import datamovie

from firebase_admin import credentials
from flask import Flask, request, render_template

firebaseConfig = {
    "apiKey": "AIzaSyB2sBdpMrtw6mPXrrrm62JfZBXuNjjZzY4",
    "authDomain": "winky-304809.firebaseapp.com",
    "databaseURL": "https://winky-304809-default-rtdb.firebaseio.com",
    "projectId": "winky-304809",
    "storageBucket": "winky-304809.appspot.com",
    "messagingSenderId": "1071928043911",
    "appId": "1:1071928043911:web:615356f3b6d0e787080b22"
}

#App configuration
app = Flask(__name__)


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)

			return render_template('Movielist.html', movies=datamovie.listmovie())
		except:
			return render_template('signin.html', us=unsuccessful)

	return render_template('signin.html')

# @app.route('/')
# def index():
#     t=

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	unsuccessful = 'Please check your credentials'
	successful = 'Login successful'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.create_user_with_email_and_password(email, password)
			return render_template('Movielist.html', movies=datamovie.listmovie())

		except:
			return render_template('signup.html', us=unsuccessful)

	return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)