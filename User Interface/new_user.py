import streamlit as st
import time
from content_based_filtering import ContentBasedRecommender
from recommend_movies import RecommendMovies
from load_data import MovieLens
import pandas as pd


# call MovieLens instance to get movie lens data
@st.cache_data
def loadMovieLensData():
    ml=MovieLens()
    data=ml.load_data()
    return ml, data

# Load MovieLens data
movies = pd.read_csv('../Movielens dataset/movies.csv')
ratings = pd.read_csv('../Movielens dataset/ratings.csv')

# extract year from the title


# make copy of ratings dataframe to store the movies rated by new user

ratingsdf=MovieLens.ratingsdf

# using the LoadMovieLens() function
ml, data = loadMovieLensData()
movie_mapping, all_movie_names = ml.merge_data()

# Create a ContentBasedRecommender instance
content_based_recommender = ContentBasedRecommender(movies, ratings)

# function to find a unique user id for new user
def find_unique_user_id(data):
    # Extract user IDs from the loaded data
    user_ids_in_data =set([uid for uid, _, _, _ in data.raw_ratings])

    # Find the maximum user ID in the dataset
    max_user_id_in_data = max(user_ids_in_data) if user_ids_in_data else 0

    # Increment the maximum user ID to get a new unique user ID
    new_user_id = max_user_id_in_data + 1

    return new_user_id


# function to assign new user id
def assign_new_user_id(data):
    # Assign new user id to new user
    new_user_id = find_unique_user_id(data)

    # Create an empty slot for the success message
    success_slot = st.empty()

    success_slot.title('Welcome new user')
    time.sleep(3)

    # Display the success message after 3 seconds (adjust the duration as needed)
    success_slot.text(f'Your assigned User ID is: {new_user_id}')
    time.sleep(3)

    # Clear the success message after the delay
    success_slot.empty()
    return new_user_id


# function for search functionality
def search_functionality(selected_movies, number_movies):
    # Ensure a movie is selected
    if selected_movies:
        # Get recommendations for the selected movie
        movie_titles, tmdbIDs, posters = content_based_recommender.contentBasedRecommender(movie_name=selected_movies, number_of_recommendation=number_movies, movie_mapping=movie_mapping)
        # print("Content based recommended movie id", movie_id)
        # Display the recommendations
        num_cols = 5  # Number of columns to display the movies
        num_rows = (number_movies + num_cols - 1) // num_cols  # Calculate the number of rows

        # Create a layout with dynamic columns and rows
        for row in range(num_rows):
            cols = st.columns(num_cols)
            with st.container():
                for col in range(num_cols):
                    index = row * num_cols + col
                    if index < len(movie_titles):
                        cols[col].image(posters[index])
                        cols[col].text(movie_titles[index])
                    else:
                        # Handle the case when there are fewer recommendations than expected
                        cols[col].empty()


# movie to show when the new user enters
def recommend_new_users():
    # using the LoadMovieLens() function

    number_movies = 20

    # title for recommended movies
    st.write("Top 20 popular movies you might like")
    movie_titles, tmdbIds, posters = RecommendMovies.content_based_recommendation(ratingsdf=ratingsdf,
                                                                                  movie_mapping=movie_mapping,
                                                                                  number_movies=number_movies)
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
                    cols[col].text(movie_titles[index])


# function to let user choose the movie and number of movies
def user_choice():
    selected_movies = st.selectbox(
        "Type or select a movie from the dropdown for recommendation",
        all_movie_names
    )
    number_movies = st.slider("Choose the number of movies to recommend", 0, 20)
    return selected_movies, number_movies


# function to get movie id by name
def get_movie_id (movie_name):
    try:
        movie_id = movies[movies['title'] == movie_name]['movieId'].index[0]
        return movie_id
    except :
        print(f"Movie with title '{movie_name}' not found in the dataset.")
        return None



# function to recommend movies when user click show recommend movies button
def content_based_recommend_movies():
    user_id=assign_new_user_id(data)
    selected_movies, number_movies=user_choice()
    if st.button("Show Recommendation"):
        st.write(f"Top {number_movies} similar movies to {selected_movies}")
        # creating a search box for movie name input for more recommendation
        search_functionality(selected_movies=selected_movies, number_movies=number_movies)

