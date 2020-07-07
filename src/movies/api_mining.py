from .keys import api_key
import requests
import json
import datetime
import pandas as pd
from . import models

# API SET UP
discover_api = "https://api.themoviedb.org/3/discover/movie?"


# Get the genres (surprisingly harder than it looks)
genres_url = "https://api.themoviedb.org/3/genre/movie/list?{}&language=en-US".format(
    api_key)
data_genres = requests.get(genres_url).json()
df_genres = pd.DataFrame(data_genres)
df_genres = pd.json_normalize(
    data=data_genres, record_path="genres").set_index("id")


def genre_to_id(genre):
    '''
    The genres from the TMDb are indexed by id. This function gets the id from
    a genre string.
    Uses a mask series on the genres (those that match)
    '''
    genre = genre.title()
    df_genre_mask = df_genres['name'].str.contains(genre)
    genre_id = df_genres.index[df_genre_mask == True].tolist()[0]

    return genre_id


# GLOBAL VARS
GENRE_OPTIONS = df_genres['name'].tolist()  # list of arrays
PAGE = 1
RATE_BY_OPTIONS = ["popularity", "release_date",
                   "revenue", "vote_average", "vote_count"]
RATE_BY = "popularity"


# Get the http request from the database as an url
def get_query(rate_by="off", desc="off", genre="off", year="off", release_date="off"):
    '''
    Prepares the query for the API as a string
    '''
    query = ""
    for arg in get_query.__code__.co_varnames:
        if arg is None:
            arg = "off"

    # process input for url requirements (see API documentation)
    try:
        rate_by = rate_by.lower()
    except:
        pass
    finally:
        if rate_by not in RATE_BY_OPTIONS:
            rate_by = "popularity"

    query += "&sort_by={}".format(rate_by) + ".desc"

    if genre in GENRE_OPTIONS:
        query += "&with_genres={}".format(genre_to_id(genre))

    try:
        int(year)
    except:
        pass
    else:
        query += "&year={}".format(year)

    if release_date != "off":
        '''
        Correcting this is gonna be fun
        '''
        (from_date, to_date) = release_date
        (year, month, day) = from_date
        from_date = datetime.date(year, month, day)

        (year2, month2, day2) = to_date
        to_date = datetime.date(year2, month2, day2)  # no time stamp

        query += "&primary_release_date.gte={}&primary_release_date.lte={}".format(
            from_date, to_date)

    query += "&page={}".format(PAGE)
    return query


def get_url(query):
    url = discover_api + api_key + query
    return url


def url_to_ls(url):
    '''
    sends the reqeusts, processes the JSON with pandas and
    makes a list of movies (each as a dictionary with info keys)
    Easy to turn into model!
    '''
    r = requests.get(url)
    if r.status_code != 200:  # API specific, see documentation
        '''Something went wrong'''
        print("Error")
        return -1

    # to json
    data_requested = r.json()
    # json_normalize
    df = pd.json_normalize(data=data_requested, record_path="results")
    df = df.set_index("id")
    # filter relevant info
    df = df[df["vote_count"] >= 500]
    df = df[["title", "genre_ids", "release_date", "overview",
             RATE_BY, "vote_count", "poster_path", "vote_average"]]

    lst = []
    for row in df.iterrows():
        dic = {
            "id": str(row[0]),
            "title": row[1]["title"],
            "genres": row[1]["genre_ids"],
            "release_date": row[1]["release_date"],
            "overview": row[1]["overview"],
            "popularity": row[1]["popularity"],
            "vote_count": row[1]["vote_count"],
            "poster_path": row[1]["poster_path"],
            "vote_average": row[1]["vote_average"]
        }
        lst.append(dic)
    return lst

####### for REST API ####


def ls_to_model_ls(ls_dic):
    '''
    Creates models
    Requires a list of dictonaries
    or should we do it directly in url_to_ls()?
    No, this way can use for api and rendering
    '''
    ls_dic = ls_dic[:10]
    for movie in ls_dic:
        # initializes models
        models.Movies(
            id=movie['id'],
            title=movie['title'],
            genres=movie['genres'],
            release_date=movie['release_date'],
            overview=movie['overview'],
            popularity=movie['popularity'],
            vote_count=movie['vote_count'],
            poster_path=movie['poster_path'],
            vote_average=movie['vote_average']
        ).save()

# also need a function to delete them!!
