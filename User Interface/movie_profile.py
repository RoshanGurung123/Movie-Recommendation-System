import streamlit as st
import pandas as pd

def display_movie_profile(movie_id):
    # load the movie dataset
    # movies=pd.read_csv('../Movielens dataset/movies.csv')
    #
    # # find the dmovie details based on movie_id
    # movie_details=movies[movies['movieId']==movie_id]
    #
    # # display the movie details
    # st.title(movie_details['title'].values[0])
    # st.write(f"Genres:")
    st.write("Welcome")


def display_movie_profile_page(selected_movie_id):
    st.title('Movie Profile')
    display_movie_profile(selected_movie_id)