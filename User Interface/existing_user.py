# importing the necessary library
import streamlit as st
import pandas as pd
from streamlit.runtime.state import SessionState

from load_data import MovieLens
from recommend_movies import RecommendMovies
from content_based_filtering import ContentBasedRecommender
import user_profile, movie_profile
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
file_path = '../final_model_svd.pkl'
movies='Movielens dataset/movies.csv'

# calling the loadMovieLensData
ml, data=loadMovieLensData()

# using the merge_data function from ml
movie_mapping, all_movie_names=ml.merge_data()


# function to execute trained Collaborative Filtering
def load_model ():
    loaded_model = pickle.load(open(file_path, 'rb'))
    return loaded_model

# Function to get the movie id using the movie name
# def get_movie_id(movie_name):
#     try:
#        movie_id = movies[movies['title'] == movie_name]['movieId'].index[0]
#        return movie_id
#     except IndexError:
#        print(f"Movie with title '{movie_name}' not found in the dataset.")
#        return None

# function for search functionality
# def search_functionality(user_id, movie_name,model,top_n=10,):
#     movie_id=content_based_recommender.get_movie_id(movie_name)
#
#     similar_movies=model.get_neighbors(movie_id, k=top_n)
#
# #     filter out the top N movies the user has already rated
#     user_watched_movies=set(data.df[data.df['user'] == user_id]['item'])
#     recommended_movies = [data.to_raw_iid(movie) for movie in similar_movies if movie not in user_watched_movies][
#                          :top_n]
#
#     print("Recommended Movies are:",recommended_movies)


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
        movie_title, predicted_ratings, tmdbIDs, posters = recommend_movies_cached(
            model=loaded_model, no_movies=number_movies, user_id=user_id,
            all_items=all_items, movie_mapping=movie_mapping
        )

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
                        cols[col].number_input(f'Rate {movie_title[index]}',1,5)


                        # css code for hovering and linking the name of the movie to get movie details
                        st.markdown("""<style>
                                button[kind="primary"] {
                                    background: none!important;
                                    border: none;
                                    padding: 0!important;
                                    color: white !important;
                                    text-decoration: none;
                                    cursor: pointer;
                                    border: none !important;
                                }
                                button[kind="primary"]:hover {
                                    text-decoration: none;
                                    color: green !important;
                                }
                                button[kind="primary"]:focus {
                                    outline: none !important;
                                    box-shadow: none !important;
                                    color: black !important;
                                }
                                </style>
                                """,
                                unsafe_allow_html=True,)
