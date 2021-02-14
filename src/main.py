#Imports

import pyrebase
from src import datamovie
from bs4 import BeautifulSoup as bs
import uuid
from flask import Flask, request, render_template
from src.user import user

global wishlist
global currentUser
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

# init()
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
listmovie=datamovie.listmovie(firebase)



##add movie to wishlist
@app.route('/Movielist', methods=['GET', 'POST'])
def Addmovie():
	global currentUser
	global wishlist
	if request.method == 'POST':
		id = request.form.get('movie_id')
		if id not in currentUser.movie:
			currentUser.movie.append(int(id))
		db = firebase.database()
		db.child("users").child(currentUser.uid).push(id)
		wishlist = datamovie.wishlistmovie(firebase, currentUser.uid,currentUser.movie)

	return render_template('Movielist.html', movies=listmovie,wish=wishlist)

##delete movie from wishlist
@app.route('/Movielistdel', methods=['GET', 'POST'])
def Deletemovie():
	global currentUser
	try:
		if request.method == 'POST':
			id = request.form.get('movie_id')
			db = firebase.database()
			db.child("users").child(currentUser.uid).child(id).delete()
	except:
		print("error")
	return render_template('Movielist.html', movies=listmovie,wish=currentUser.movie)





#sign in to app Engine
@app.route('/', methods=['GET', 'POST'])
def signin():
	global currentUser
	unsuccessful = 'Please check your credentials'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)
			id=auth.current_user.get("localId")
			currentUser = user(email, [],id)
			currentUser.movie = datamovie.wishlist(firebase, currentUser.uid)
			return render_template('Movielist.html', movies=listmovie,wish=currentUser.movie)
		except:
			return render_template('signin.html', us=unsuccessful)

	return render_template('signin.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	global currentUser
	unsuccessful = 'Please check your credentials'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.create_user_with_email_and_password(email, password)
			return render_template('Movielist.html', movies=listmovie,wish=currentUser.movie)
		except:
			return render_template('signup.html', us=unsuccessful)
	return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)