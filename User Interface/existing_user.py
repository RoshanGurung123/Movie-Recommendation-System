# importing the necessary library
import streamlit as st
import pandas as pd
from load_data import MovieLens
from recommend_movies import RecommendMovies
from content_based_filtering import ContentBasedRecommender
import pickle
import time


# Load MovieLens data
movies = pd.read_csv('../Movielens dataset/movies.csv')
ratings = pd.read_csv('../Movielens dataset/ratings.csv')


# create an instance of ContentBasedRecommender
content_based_recommender=ContentBasedRecommender(movies, ratings)


# call MovieLens instance to get movie lens data
def loadMovieLensData():
    ml=MovieLens()
    data=ml.load_data()
    return ml, data

# declare file path for saved model
file_path = '../Trained model/final_model_svd.pkl'
movies='Movielens dataset/movies.csv'

# calling the loadMovieLensData
ml, data=loadMovieLensData()

# using the merge_data function from ml
movie_mapping, all_movie_names=ml.merge_data()


# function to execute trained Collaborative Filtering
def load_model ():
    loaded_model = pickle.load(open(file_path, 'rb'))
    return loaded_model

def recommend_movies_cached(model, no_movies, user_id, all_items, movie_mapping):
    return RecommendMovies.recommend_movies(model, no_movies, user_id, all_items, movie_mapping)


def recommendation_existing_user():
    st.title('Movie Recommendation System')
    # user id input field

    user_id = st.number_input('Enter User ID', min_value=1, max_value=610, value=1)
    # creating a slider menu
    number_movies = st.slider('Choose the number of movies to recommend', 1, 20)

    # call function
    loaded_model = load_model()
    trainset, testset, all_items = ml.trainTestSplit()

    if st.button("Show recommendation"):
        st.write(f"{number_movies} movies recommended for you")
        movie_title, predicted_ratings, tmdbIDs, posters = RecommendMovies.recommend_movies(
            model=loaded_model, no_movies=number_movies, user_id=user_id,
            all_items=all_items, movie_mapping=movie_mapping, ratingsdf=ratings
        )
        print('Movie title', movie_title)
        print('Movie id', tmdbIDs)
        print('predicted ratings', predicted_ratings)

        # st.sidebar.button('Usersss')
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


