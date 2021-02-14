import json
import os

import requests

from src.Movie import Movie


# token here
# def initalmovie(fb):
#     id=0;
#     db = fb.database()
#     x = requests.get('https://itunes.apple.com/us/rss/topmovies/limit=25/json')
#     y=json.loads(x.content)
#     movies = y.get("feed").get("entry")
#     for movie in movies:
#         name = movie.get("im:name").get("label")
#         summary = movie.get("im:name").get("label")
#         image = movie.get("im:image")[0].get("label")
#         try:
#             moviedetials = {"name": name, "image": image,"id":id}
#             id=id+1
#             db.child("movies").push(moviedetials)
#         except:
#             print("er")
#

def listmovie(fb):
    list=[]
    db = fb.database()
    movies=db.child("movies").get()

    for x in movies.each():
        name=x.val().get("name")
        image=x.val().get("image")
        id=x.val().get("id")
        MovieCon=Movie("T",name,image,id)
        list.append(MovieCon)
    return list

def wishlistmovie(fb,localid,listlocal):
    list=[]
    print(listlocal)
    db = fb.database()
    movies=db.child("movies").get()
    for x in movies.each():
        id = x.val().get("id")
        if id in listlocal:
            name = x.val().get("name")
            image = x.val().get("image")
            MovieCon = Movie("T", name, image, id)
            list.append(MovieCon)
    print(list)
    return list

def wishlist(fb,name):
    db = fb.database()
    try:
        movies = db.child("users").child(name).get()
        for x in movies.each():
            id = x.val().get("id")
            list.append(id)
        print(list)
    except:
        return []
    return list

def findmovie(fb,id):
    db = fb.database()
    movies = db.child("movies").get()
    MovieCon=""
    for x in movies.each():
        idnum=x.val().get("id")
        if(id==str(idnum)):
            name = x.val().get("name")
            image = x.val().get("image")
            MovieCon = Movie("T", name, image, idnum)
    return MovieCon





