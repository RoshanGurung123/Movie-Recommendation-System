from LoadData import MovieLens
import pandas as pd
import streamlit as st
from Recommendmovies import RecommendMovies
import pickle

# call MovieLens function to get movie lens data
def loadMovieLensData():
    ml=MovieLens()
    data=ml.load_data()
    return ml, data



# declare file path for saved model
file_path = 'final_model_svd.pkl'

# function to execute user-based Collaborative Filtering
def load_model ():
    loaded_model = pickle.load(open(file_path, 'rb'))
    return loaded_model

# Function to find a unique user ID not present in the dataset
def find_unique_user_id(data):
    # Extract user IDs from the loaded data
    user_ids_in_data =set([uid for uid, _, _, _ in data.raw_ratings])

    # Find the maximum user ID in the dataset
    max_user_id_in_data = max(user_ids_in_data) if user_ids_in_data else 0

    # Increment the maximum user ID to get a new unique user ID
    new_user_id = max_user_id_in_data + 1

    return new_user_id


# Function for the sign-up screen
def sign_up_screen(data):
    st.title('Sign Up')

    new_user_id = find_unique_user_id(data)

    st.write(f'Your assigned User ID is: {new_user_id}')

    if st.button('Sign Up'):
        st.success(f'Welcome, User {new_user_id}')
        st.markdown('User created successfully!')

        # Save the new_user_id or perform any other necessary actions
def content_based_recommendation():


# Function for the main recommendation screen
def main_recommendation_screen(user_id):
    st.title('Movie Recommendation System')

    ml, data = loadMovieLensData()

    # creating a sidebar menu

    number_movies = st.slider('Choose the number of movies to recommend', 0, 20)

    # call function
    loaded_model = load_model()
    trainset, testset, all_items = ml.trainTestSplit()
    movie_mapping = ml.merge_data()

    if st.button("Show recommendation"):
        movie_title, predicted_ratings, tmdbIDs, posters = RecommendMovies.recommend_movies(
            model=loaded_model, no_movies=number_movies, user_id=user_id,
            all_items=all_items, movie_mapping=movie_mapping
        )
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

# main function
def main():
    ml, data = loadMovieLensData()
    # Check if it's a new user
    menu = st.sidebar.selectbox("Menu", ['Existing User', 'New User'])

    if menu=="New User":
        sign_up_screen(data)
    else:
        # For existing users, show the main recommendation screen
        user_id = st.sidebar.number_input('Enter User ID', min_value=1, max_value=1000, value=1)
        # main_recommendation_screen(user_id)
        main_recommendation_screen(user_id)

if __name__ == "__main__":
    main()