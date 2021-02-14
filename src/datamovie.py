import json

import requests

from src.Movie import Movie



def listmovie():
    # storage=firebase.storage()

    list=[]
    x = requests.get('https://itunes.apple.com/us/rss/topmovies/limit=25/json')
    y=json.loads(x.content)
    movies=y.get("feed").get("entry")
    for movie in movies:
        name=movie.get("im:name").get("label")
        summary=movie.get("im:name").get("label")
        image=movie.get("im:image")[0].get("label")
        # storage.child("images").put(image)

        MovieCon=Movie(summary,name,image)
        list.append(MovieCon)

    return list

