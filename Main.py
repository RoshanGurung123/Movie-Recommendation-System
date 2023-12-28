from LoadData import MovieLens
import pandas as pd
import streamlit as st
from Recommendmovies import RecommendMovies
import pickle
from ContentBasedRecommendation import ContentBasedRecommender
import time

# call MovieLens instance to get movie lens data
def loadMovieLensData():
    ml=MovieLens()
    data=ml.load_data()
    return ml, data

ratingsdf=MovieLens.ratingsdf


# declare file path for saved model
file_path = 'final_model_svd.pkl'

# Load MovieLens data
movies = pd.read_csv('Movielens dataset/movies.csv')
ratings = pd.read_csv('Movielens dataset/ratings.csv')

ratings_copy=ratings.copy()


# Create a ContentBasedRecommender instance
content_based_recommender = ContentBasedRecommender(movies, ratings)

# calling the loadMovieLensData
ml, data=loadMovieLensData()

# using the merge_data function from ml
movie_mapping, all_movie_names=ml.merge_data()

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

# Function to recommend movies to new user

def recommend_new_users(new_user_id, number_movies):

    # using the LoadMovieLens() function
    ml, data=loadMovieLensData()
    movie_mapping, all_movie_names=ml.merge_data()
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
    # if st.button("Show recommendation"):



# Function for the sign-up screen
def sign_up_screen(data):
    # Assign new user id to new user
    new_user_id = find_unique_user_id(data)

    # Create an empty slot for the success message
    success_slot = st.empty()

    success_slot.title('Welcome new user')
    time.sleep(10)

    # Display the success message after 3 seconds (adjust the duration as needed)
    success_slot.text(f'Your assigned User ID is: {new_user_id}')
    time.sleep(7)

    # Clear the success message after the delay
    success_slot.empty()
    # # Ask the user to rate movies
    # st.write(f"Rate at least 10 movies to unlock personalized recommendations for User ID: {new_user_id}")
    #
    # # Create a list to store new user ratings
    # new_user_ratings = []
    #
    # for i in range(10):
    #     movie_id = st.selectbox('Select a movie to rate:', all_movie_names)
    #     rating = st.slider(f'Rate {movie_id} (1-5):', 1, 5)
    #     timestamp = int(time.time())
    #
    #     # Add the rating to the new_user_ratings list
    #     new_user_ratings.append({'userId': new_user_id, 'movieId': movie_mapping[movie_id], 'rating': rating, 'timestamp': timestamp})
    #
    # # Convert the list of dictionaries to a DataFrame
    # new_user_ratings_df = pd.DataFrame(new_user_ratings)
    #
    # # Concatenate the existing ratings dataframe with the new user ratings
    # new_ratingsdf = pd.concat([ratings_copy, new_user_ratings_df], ignore_index=True)
    #
    # new_ratingsdf.to_csv('Movielens dataset/updated_data.csv')
    return new_user_id

# Function for the main recommendation screen
def main_recommendation_screen(user_id):
    st.title('Movie Recommendation System')

    ml, data = loadMovieLensData()

    # creating a sidebar menu

    number_movies = st.slider('Choose the number of movies to recommend', 0, 20)

    # call function
    loaded_model = load_model()
    trainset, testset, all_items = ml.trainTestSplit()
    # movie_mapping = ml.merge_data()

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

def search_functionality(selected_movies, number_movies):
    # Ensure a movie is selected
    if selected_movies:
        # Get recommendations for the selected movie
        movie_titles, tmdbIDs, posters = content_based_recommender.contentBasedRecommender(movie_name=selected_movies, number_of_recommendation=number_movies, movie_mapping=movie_mapping)

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


def movie_profile(movie_id):
    movie_details=movies[movies['movieId'] == movie_id].iloc[0]
    st.title(f"{movie_details['title']}")

#     display movie details
    st.write(f"**Title:** {movie_details['title']}")
    st.write(f"**Genres:** {movie_details['genres']}")



# main function
def main():
    ml, data = loadMovieLensData()

    movie_mapping, all_movie_names = ml.merge_data()
    # Check if it's a new user
    menu = st.sidebar.selectbox("Menu", ['Existing User', 'New User'])

    # Use session state to persist variables between runs
    if menu == "New User":
        # assigning new user id to new user
        user_id = sign_up_screen(data)

        selected_movies = st.sidebar.selectbox(
            "Type or select a movie from the dropdown for recommendation",
            all_movie_names
        )
        # slider for user to choose the number of movies they want
        number_movies = st.sidebar.slider('Choose the number of movies to recommend', 0, 20)

        if st.sidebar.button('Search recommendation'):
            st.write(f"Top {number_movies} similar movies to {selected_movies}")
            # creating a search box for movie name input for more recommendation
            search_functionality(selected_movies=selected_movies, number_movies=number_movies)
        elif st.button('Show Recommendation'):
            number_movies=20
            recommend_new_users(user_id, number_movies)

        # Display user ID at the menu
        st.sidebar.markdown(f"**User ID:** {user_id}")

    else:
        # For existing users, show the main recommendation screen collaborative filtering
        user_id = st.sidebar.number_input('Enter User ID', min_value=1, max_value=1000, value=1)
        # main_recommendation_screen(user_id)
        main_recommendation_screen(user_id)

        # Check if a movie is selected for the movie profile page
        selected_movie_id = st.selectbox("Select a movie for detailed profile", movie_mapping.keys())


if __name__ == "__main__":
    main()