# importing necessary libraries
import streamlit as st
from tmdbv3api import TMDb, Movie
import pandas as pd
from surprise import dump
from surprise import SVD, Reader, Dataset
from surprise.model_selection import train_test_split
import pickle
import LoadData


# Load datasets
moviesdf = pd.read_csv('Movielens dataset/movies.csv')
ratingsdf = pd.read_csv('Movielens dataset/ratings.csv')
linksdf=pd.read_csv('Movielens dataset/links.csv')
reader = Reader(rating_scale=(1, 5))

data = Dataset.load_from_df(ratingsdf[['userId', 'movieId', 'rating']], reader)

# splitting the dataset into train and test set
trainset, testset = train_test_split(data, test_size=0.25, random_state=42)

all_items = trainset.all_items()

## Load the trained SVD model
model_filename = 'final_model_svd.pkl'
loaded_model=pickle.load(open(model_filename,'rb'))
# function to fetch movie posters
tmdb = TMDb()
tmdb.api_key = '9b799ab26d05d3bfc18975a3607bcfa9'

movie = Movie()


def fetch_poster(movie_id):
    movie_details = movie.details(movie_id)
    poster_path = movie_details.poster_path
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = fetch_poster(112)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

# merge the moviesdf and linksdf to get tmdbid
final_moviedf=moviesdf.merge(linksdf, on='movieId')

# code for mapping the movie id to get movie title
movie_mapping = dict(zip(final_moviedf['movieId'].astype(str), final_moviedf['tmdbId']))

# function to recommend movies using collaborative filtering
def recommend_movies(model, no_movies, user_id, all_items, movie_mapping):
    # Get the list of items rated by the specific user
    rated_items_by_user = [item for item, _ in trainset.ur[trainset.to_inner_uid(user_id)]]

    # Get the list of items not rated by the user
    items_not_rated_by_user = list(set(all_items) - set(rated_items_by_user))

    # Make predictions for the items not rated by the user
    item_predictions = [model.predict(user_id, item_id) for item_id in items_not_rated_by_user]

    # Sort the predictions by estimated rating
    sorted_predictions = sorted(item_predictions, key=lambda x: x.est, reverse=True)

    # Get the top N recommendations
    top_n_recommendations = sorted_predictions[:no_movies]

    movie_titles = []
    predicted_ratings = []
    tmdbIDs=[]
    posters=[]

    for recommendation in top_n_recommendations:
        item_id = str(recommendation.iid)
        movie_title = movie_mapping.get(item_id, 'Unknown Movie')
        TMDBID=movie_mapping.get(item_id, 'Unknown ID')

        # get movie details
        movies=movie.details(TMDBID)


        movie_titles.append(movies.title)
        predicted_ratings.append(recommendation.est)
        tmdbIDs.append(TMDBID)
        posters.append(fetch_poster(TMDBID))

    return movie_titles, predicted_ratings, tmdbIDs, posters

st.title('Movie Recommendation System')

# create a user input to input user id
user_id = st.number_input('Enter User ID', min_value=1, max_value=1000, value=1)

# creating a sidebar menu
new_user=st.sidebar.selectbox("New user")

number_movies=st.slider('Choose the number of movies to recommend',0,20)

if st.button("Show recommendation"):
    movie_title, predicted_ratings, tmdbIDs, posters = recommend_movies(model=loaded_model, no_movies=number_movies, user_id=user_id,
                                                all_items=all_items, movie_mapping=movie_mapping)
    num_cols = 5  # Number of columns to display the movies
    num_rows = (number_movies + num_cols - 1) // num_cols  # Calculate the number of rows

    # Create a layout with dynamic columns and rows
    for row in range(num_rows):
        cols = st.columns(num_cols)
        with st.container():
            for col in range(num_cols):
                index = row * num_cols + col
                if index < number_movies:
                    cols[col].image(posters[index])
                    cols[col].text(movie_title[index])
