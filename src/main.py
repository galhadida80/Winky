#Imports

import pyrebase
from flask import Flask, request, render_template
import  requests
import json

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
class Movie:

    def __init__(self,name,image,id,rate):
        self.rate=rate
        self.name=name
        self.image=image
        self.id=id


class user:
    def __init__(self,email,movie,uid):
        self.email=email
        self.movie=movie
        self.uid=uid

# def createUsers():
# 	for i in range(100):
# 		email = ''.join(random.choice(string.ascii_letters) for x in range(7)) + '@Winky.com'
# 		password = ''.join(random.choice(string.ascii_letters) for x in range(7))
# 		try:
# 			id=auth.create_user_with_email_and_password(email, password)
# 			f=id.get("localId")
# 			randomlist = random.sample(range(0, 24), 5)
# 			db = firebase.database()
#
# 			db.child("users").child(f).set(randomlist)
#
# 			print(f)
# 		except:
# 			print("problem with create 1000 users")
#
# def analysisRating():
# 	list=[0]*25
# 	Rateusers=firebase.database().child("users").get()
# 	for x in Rateusers.each():
# 		for index in x.val():
# 			list[int(index)]=list[int(index)]+1
# 	return list
#
#
#
#
#
#
# def initalmovie():
#     createUsers()
#     rateList=analysisRating()
#     id=0;
#     st = firebase.storage()
#     db = firebase.database()
#     x = requests.get('https://itunes.apple.com/us/rss/topmovies/limit=25/json')
#     y=json.loads(x.content)
#     movies = y.get("feed").get("entry")
#     for movie in movies:
#         name = movie.get("im:name").get("label")
#         image = movie.get("im:image")[0].get("label")
#
#         response = requests.get(image, stream=True)
#         with open('img.png', 'wb') as out_file:
#             shutil.copyfileobj(response.raw, out_file)
#         t=st.child(name).put('img.png')
#
#         image=st.child(name).get_url(None)
#         rate=rateList[id]/10
#         moviedetials = {"name": name, "image": image,"id":id,"rate":rate}
#         id=id+1
#         db.child("movies").push(moviedetials)






def AllMovies():

    list=[]
    db = firebase.database()
    movies=db.child("movies").get()

    for x in movies.each():
        name=x.val().get("name")
        rate=x.val().get("rate")
        image=x.val().get("image")
        id=x.val().get("id")
        MovieCon=Movie(name,image,id,rate)
        list.append(MovieCon)
    return list

def wishlistmovie(privatelist):
    list=[]
    print("wish")
    print(privatelist)


    if len(privatelist) == 0:
        return []
    db = firebase.database()
    movies=db.child("movies").get()
    for x in movies.each():
        id=x.val().get("id")
        if str(id) in privatelist:
            name = x.val().get("name")
            rate = x.val().get("rate")
            image = x.val().get("image")
            id = x.val().get("id")
            MovieCon = Movie(name, image, id, rate)
            list.append(MovieCon)
    print(list)
    return list





def initWishListByID(name):
	db = firebase.database()
	list=[]
	try:
		movies = db.child("users").child(name).get()
		for x in movies.each():
			list.append(x.val())
	except:
		return[]
	return list





# initalmovie()

listmovie=AllMovies()



##add movie to wishlist
@app.route('/Movielist', methods=['GET', 'POST'])
def Addmovie():
	global currentUser
	global wishlist
	if request.method == 'POST':
		print(currentUser.movie)

		id = request.form.get('movie_id')
		print(id)
		if str(id) not in currentUser.movie:
			currentUser.movie.append(id)
			print(id)
		db = firebase.database()
		db.child("users").child(currentUser.uid).set(currentUser.movie)
		wishlist = wishlistmovie(currentUser.movie)
		print("addmovie")
		print(wishlist)
	return render_template('Movielist.html', movies=listmovie,wish=wishlist)

##delete movie from wishlist
@app.route('/Movielistdel', methods=['GET', 'POST'])
def Deletemovie():
	global currentUser
	global wishlist

	if request.method == 'POST':
		id = request.form.get('movie_id')
		print(id)
		db = firebase.database()
		currentUser.movie.remove(id)
		try:

		    db.child("users").child(currentUser.uid).remove()
		except:
			print("error")
		db.child("users").child(currentUser.uid).set(currentUser.movie)
		wishlist = wishlistmovie(currentUser.movie)

	return render_template('Movielist.html', movies=listmovie,wish=wishlist)





#sign in to app Engine
@app.route('/', methods=['GET', 'POST'])
def signin():
	global currentUser
	global wishlist

	unsuccessful = 'Please check your credentials'
	if request.method == 'POST':
		email = request.form['name']
		password = request.form['pass']
		try:
			auth.sign_in_with_email_and_password(email, password)
			id=auth.current_user.get("localId")
			currentUser = user(email, [],id)
			currentUser.movie = initWishListByID(currentUser.uid)
			wishlist=wishlistmovie(currentUser.movie)
			return render_template('Movielist.html', movies=listmovie,wish=wishlist)
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


# createUsers()
if __name__ == '__main__':
	#send movie to firebase
    app.run(debug=True)