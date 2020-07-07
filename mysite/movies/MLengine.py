import pandas as pd
import requests
import json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# best kept private
from .keys import api_key


# What will be used to calculate similarity scores
FEATURES = ["title", "overview"]
discover_api = "https://api.themoviedb.org/3/discover/movie?"


def page_url(page=1):
    '''
    Uses default query specifications
    '''
    query = "&language=en-US&sort_by=popularity.desc&include_adult=false&page={}&vote_count.gte=500".format(
        page)
    url = discover_api + api_key + query
    return url


def make_big_dataframe(max_pages=10):
    '''
    The API proides data in pages of 10 movies per url request.
    This function iterates over each page adding the data to one big pandas df
    '''
    if (max_pages >= 214):
        print("max is 213")
        return

    frames = []

    for page_num in range(1, max_pages + 1):
        url = page_url(page_num)
        r = requests.get(url)
        if r.status_code != 200:
            '''Something went wrong'''
            print("Error")
            return
        data = r.json()
        # normalize, as you convert to df
        page_df = pd.json_normalize(data=data, record_path="results")
        frames.append(page_df)

    # concat dfs into one
    df = pd.concat(frames)  # method takes array of df

    # process
    df = df.reset_index()  # (else they restart at 19)
    df = df[["title",
             "genre_ids",
             "release_date",
             "overview",
             "popularity",
             "vote_count",
             "poster_path",
             "vote_average"]]
    return df


def combine_features(row):
    combined_str = ""
    for feat in FEATURES:
        combined_str += row[feat] + " "
    return combined_str
#######################################
# df["combined_features"] = df.apply(combine_features,axis=1) #applying combined_features() method over each rows of dataframe and storing the combined string in "combined_features" column
##########################################

# HELPER functions


def get_title_from_index(index, df):
    return df[df.index == index]["title"].values[0]


def get_index_from_title(title, df):
    # should iterate over all and see if coantains string
    title = title.title()
    return df[df.title == title].index.values[0]


def get_cos_similarity_matrix(df, movie_user_likes):
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(df["combined features"])
    cosine_matrix = cosine_similarity(count_matrix)

    movie_index = get_index_from_title(movie_user_likes, df)
    similar_movies = list(enumerate(cosine_matrix[movie_index]))

    sorted_similar_movies = sorted(
        similar_movies, key=lambda x: x[1], reverse=True)
    return sorted_similar_movies
